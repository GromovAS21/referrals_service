from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from referral_cods.models import Referral
from referral_cods.permissions import IsOwner
from referral_cods.serializers import ReferralCodeSerializer


class CreateReferralCodeView(generics.CreateAPIView):
    """Создание реферального кода"""

    serializer_class = ReferralCodeSerializer
    queryset = Referral.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeleteReferralCodeView(generics.DestroyAPIView):
    """Удаление реферального кода"""

    queryset = Referral.objects.all()
    permission_classes = (IsOwner,)


class SendEmailReferralCodeView(APIView):
    """Отправка реферального кода на email"""

    def post(self, request):

        user = request.user

        try:
            referral_cod = Referral.objects.get(owner=user)
        except Referral.DoesNotExist:
            return Response({"message": "Реферальный код еще не создан"})

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