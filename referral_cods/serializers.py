from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from referral_cods.models import Referral
from users.serializers import UserSerializer


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания реферального кода"""

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Referral
        fields = ("id", "code", "validity_period", "active", "owner")

    def create(self, validated_data):
        owner = self.context['request'].user
        if Referral.objects.filter(owner=owner, active=True).exists():
            raise ValidationError({"active": "Вы уже имеете активный реферальный код, для создания нового кода необходимо удалить имеющийся код."})
        return super().create(validated_data)

