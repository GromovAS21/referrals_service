from rest_framework import generics
from rest_framework.permissions import AllowAny

from referral_cods.models import Referral
from users.models import User
from users.serializers import UserDetailSerializer


class UserCreateView(generics.CreateAPIView):
    """Создание пользователя который  имеет реферальный код"""

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save(update_fields=["password"])

            # Берем реферальный код, с помощью которого произведена регистрация
            referral_code = serializer.initial_data["referral_code"]
            # Находим пользователя, которому принадлежит реферальный код
            referer_user = Referral.objects.get(code=referral_code).owner
            # Добавляем к владельцу реферального кода нового зарегистрированного пользователя в качестве реферала
            referer_user.referral_users.add(user)
            referer_user.save()




