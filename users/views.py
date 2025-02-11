from rest_framework import generics
from rest_framework.permissions import AllowAny

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


