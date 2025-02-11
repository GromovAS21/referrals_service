from rest_framework import serializers

from referral_cods.models import Referral
from users.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    password = serializers.CharField(write_only=True, min_length=8)
    referral_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "referral_code")

    def create(self, validated_data):

        referral_code = validated_data.pop("referral_code")

        if Referral.objects.filter(code=referral_code, active=True).exists():
            return super().create(validated_data)
        else:
            raise serializers.ValidationError({"referral_code": "Такого реферального кода не существует"})
