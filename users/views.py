from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

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

            # Берем реферальный код, с помощью которого произведена регистрация
            referral_code = serializer.initial_data["referral_code"]
            # Находим пользователя, которому принадлежит реферальный код
            referer_user = Referral.objects.get(code=referral_code).owner
            # Добавляем к владельцу реферального кода нового зарегистрированного пользователя в качестве реферала
            user.referer_user = referer_user

            referer_user.save()
            user.save(update_fields=["password", "referer_user"])


class AllReferralUsersView(APIView):
    """Получение всех приглашенных пользователей у текущего пользователя"""

    def get(self, request):

        user = request.user
        referral_users = user.referral_users.all()
        if referral_users:
            users_list = list(referral_users.values("id", "email"))
            return Response(users_list, status=HTTP_200_OK)
        else:
            return Response({"message": "Приглашенных пользователей нет"}, status=HTTP_200_OK)




