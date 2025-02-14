from rest_framework import serializers

from referral_cods.models import ReferralCode
from users.models import User
from users.services import verify_email


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    password = serializers.CharField(write_only=True, min_length=8)
    referral_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "referral_code")

    def create(self, validated_data):
        email = validated_data["email"]
        # Проверка на существующий email
        if not verify_email(email):
            raise serializers.ValidationError({"email": "Email не валиден"})

        referral_code = validated_data.pop("referral_code")

        # Проверка на существующий реферальный код
        if not ReferralCode.objects.filter(code=referral_code, active=True).exists():
            raise serializers.ValidationError({"referral_code": "Такого реферального кода не существует"})

        return super().create(validated_data)
