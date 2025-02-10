from rest_framework import serializers

from referral_cods.models import Referral
from referral_cods.validators import ActiveReferralCodeValidator, validate_date_in_past


class CreateReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания реферального кода"""

    class Meta:
        model = Referral
        fields = ("code", "validity_period",)
        validators = [
            ActiveReferralCodeValidator(owner=serializers.CurrentUserDefault()),
            validate_date_in_past
        ]

