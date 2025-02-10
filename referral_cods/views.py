from rest_framework import generics

from referral_cods.models import Referral
from referral_cods.serializers import CreateReferralCodeSerializer


class CreateReferralCodeView(generics.CreateAPIView):
    """Создание реферального кода"""

    serializer_class = CreateReferralCodeSerializer
    queryset = Referral.objects.all()


class DeleteReferralCodeView(generics.DestroyAPIView):
    """Удаление реферального кода"""

    queryset = Referral.objects.all()