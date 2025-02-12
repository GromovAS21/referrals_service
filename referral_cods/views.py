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
        serializer.save(owner=self.request.user)


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

        try:
            # Проверка наличия активного реферального кода
            referral_code = ReferralCode.objects.get(owner=user, active=True)
        except ReferralCode.DoesNotExist:
            return Response({"message": "Активный реферальный код отсутствует"})

        else:
            # Создание словаря с данными реферального кода
            referral_code_data = {
                "code": referral_code.code,
                "validity_period": referral_code.validity_period
            }
            # Получение email пользователя
            email_user = user.email
            # Отправка реферального кода на email
            send_referral_code_email.delay(referral_code_data, email_user)
            return Response({"message": "Сообщение отправлено на Ваш Email"})
