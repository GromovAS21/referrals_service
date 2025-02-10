from rest_framework import generics


class UserCreateView(generics.CreateAPIView):
    """Создание пользователя который прошел по реферальной ссылке"""

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save(update_fields=["password"])


