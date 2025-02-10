from rest_framework import serializers

from referral_cods.models import Referral
from users.serializers import UserSerializer


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания реферального кода"""

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Referral
        fields = ("id", "code", "validity_period", "active", "owner")
