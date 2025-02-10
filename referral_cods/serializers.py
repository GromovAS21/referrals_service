from rest_framework import serializers

from referral_cods.models import Referral


class CreateReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания реферального кода"""

    class Meta:
        model = Referral
        fields = ("code", "validity_period",)


