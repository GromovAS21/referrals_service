from rest_framework import serializers

from users.models import User


class UserResponseSerializer(serializers.ModelSerializer):
    """Сериализатор для успешного ответа, исключает поля password и referral_code"""

    class Meta:
        model = User
        fields = ("id", "email")