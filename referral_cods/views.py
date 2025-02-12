from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from referral_cods.models import ReferralCode
from referral_cods.permissions import IsOwner
from referral_cods.serializers import ReferralCodeSerializer
from referral_cods.tasks import send_referral_code_email


class CreateReferralCodeView(generics.CreateAPIView):

    serializer_class = ReferralCodeSerializer
    queryset = ReferralCode.objects.all()

    @swagger_auto_schema(
        operation_description="Создание реферального кода авторизированным пользователем",
        operation_summary="Создание реферального кода",
        request_body=ReferralCodeSerializer,
        tags=["Реферальный код"],
        responses={
            201: openapi.Response(
                description="Пользователь успешно создан",
                schema=ReferralCodeSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        referral_code = serializer.save()
        referral_code.owner=self.request.user
        referral_code.save()
        # Добавление реферального кода в хэш
        cache.set(f"referral_code_{self.request.user.id}", referral_code.code, timeout=24*60*60)
        cache.set(f"validity_period_{self.request.user.id}", referral_code.validity_period, timeout=24*60*60)

class DeleteReferralCodeView(generics.DestroyAPIView):

    queryset = ReferralCode.objects.all()
    permission_classes = (IsOwner,)

    @swagger_auto_schema(
        operation_description="Удаление реферального кода который принадлежит текущему пользователю",
        operation_summary="Удаление реферального кода",
        tags=["Реферальный код"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор реферального кода в базе данных",
                required=True,
            )
        ],
        responses={
            204: openapi.Response(
                description="Пользователь успешно удален",
            ),
            400: "Ошибка валидации",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SendEmailReferralCodeView(APIView):

    @swagger_auto_schema(
        operation_description="Отправка активного реферального кода на email текущего пользователя",
        operation_summary="Отправка реферального кода на email",
        tags=["Реферальный код"],
        responses={
            201: openapi.Response(
                description="Реферальный код успешно отправлен",
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request):

        user = request.user
        # Проверка хэша на наличии реферального кода
        referral_code = cache.get(f"referral_code_{user.id}")
        validity_period = cache.get(f"validity_period_{user.id}")
        # Если нет в хэше
        if not referral_code and validity_period:

            try:
                # Проверка наличия активного реферального кода в БД
                referral_code_obj = ReferralCode.objects.get(owner=user, active=True)
                referral_code = referral_code_obj.code
                validity_period = referral_code_obj.validity_period
            except ReferralCode.DoesNotExist:
                return Response({"message": "Активный реферальный код отсутствует"})

        # Создание словаря с данными реферального кода
        referral_code_data = {
            "code": referral_code,
            "validity_period": validity_period
        }
        # Получение email пользователя
        email_user = user.email
        # Отправка реферального кода на email
        send_referral_code_email.delay(referral_code_data, email_user)
        return Response({"message": "Сообщение отправлено на Ваш Email"})
