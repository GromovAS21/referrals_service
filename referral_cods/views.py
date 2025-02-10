from rest_framework import generics
from referral_cods.models import Referral
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