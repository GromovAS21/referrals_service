from rest_framework import serializers

from users.models import User


class CreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = User
        fields = ("email", "password")

