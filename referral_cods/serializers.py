from rest_framework import serializers

from referral_cods.models import Referral
from referral_cods.validators import validate_date_in_past


class CreateReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания реферального кода"""

    class Meta:
        model = Referral
        fields = ("code", "validity_period",)
        validators = [
            validate_date_in_past
        ]

