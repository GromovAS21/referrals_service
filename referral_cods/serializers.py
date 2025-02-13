from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from referral_cods.models import ReferralCode
from users.serializers import UserDetailSerializer


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания реферального кода"""

    owner = UserDetailSerializer(read_only=True)

    class Meta:
        model = ReferralCode
        fields = ("id", "code", "validity_period", "active", "owner")
        read_only_fields = ("active",)

    def create(self, validated_data):
        owner = self.context["request"].user
        if ReferralCode.objects.filter(owner=owner, active=True).exists():
            raise ValidationError(
                {
                    "message": "Вы уже имеете активный реферальный код, для создания нового кода "
                    "необходимо удалить имеющийся код."
                }
            )
        return super().create(validated_data)
