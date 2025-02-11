from django.core.mail import send_mail
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from referral_cods.models import Referral
from referral_cods.permissions import IsOwner
from referral_cods.serializers import ReferralCodeSerializer


class CreateReferralCodeView(generics.CreateAPIView):

    serializer_class = ReferralCodeSerializer
    queryset = Referral.objects.all()

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

    queryset = Referral.objects.all()
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
            referral_cod = Referral.objects.get(owner=user, active=True)
        except Referral.DoesNotExist:
            return Response({"message": "Активный реферальный код отсутствует"})

        else:
            # Отправка реферального кода на email
            send_mail(
                subject="Реферальный код",
                message=f"Твой реферальный код: {referral_cod.code}"
                        f"Срок годности этого кода: {referral_cod.validity_period}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]

            )
            return Response({"message": "Сообщение отправлено на Ваш Email"})