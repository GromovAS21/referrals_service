from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from referral_cods.models import ReferralCode
from referral_cods.permissions import IsOwner
from referral_cods.serializers import ReferralCodeSerializer
from referral_cods.services import ReferralCodeService
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
                schema=ReferralCodeSerializer(),
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        referral_code = serializer.save(owner=self.request.user)
        # Добавление реферального кода в хэш
        cache.set(
            f"referral_code_{self.request.user.id}",
            referral_code.code,
            timeout=24 * 60 * 60,
        )
        cache.set(
            f"validity_period_{self.request.user.id}",
            referral_code.validity_period,
            timeout=24 * 60 * 60,
        )


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
    def delete(self, request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # Удаление из кеша
        cache.delete(f"referral_code_{self.request.user.id}")
        cache.delete(f"validity_period_{self.request.user.id}")
        super().perform_destroy(instance)


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
    def post(self, request) -> Response:

        user = request.user

        referral_code_data = ReferralCodeService.get_referral_code_data(user)
        if not referral_code_data:
            return Response({"message": "Активный реферальный код отсутствует"})

        # Получение email пользователя
        email_user = ReferralCodeService.get_user_email(user)
        # Отправка реферального кода на email
        send_referral_code_email.delay(referral_code_data, email_user)
        return Response({"message": "Сообщение отправлено на Ваш Email"})
