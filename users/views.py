from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from referral_cods.models import Referral
from users.models import User
from users.seializers_swagger import UserResponseSerializer
from users.serializers import UserDetailSerializer


class UserCreateView(generics.CreateAPIView):

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Создание пользователя который имеет реферальный код",
        operation_summary="Создание нового пользователя",
        request_body=UserDetailSerializer,
        tags=["Пользователь"],
        responses={
            201: openapi.Response(
                description="Пользователь успешно создан",
                schema=UserResponseSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_description="Получение всех приглашенных пользователей у текущего пользователя",
        operation_summary="Список приглашенных пользователей",
        tags=["Пользователь"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка приглашенных пользователей",
                schema=UserResponseSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request):

        user = request.user
        # Получаем всех пользователей, где текущий пользователь числится referer_user
        referral_users = user.referral_users.all()

        if referral_users:
            # Выводим списком из словарей с полями id, email
            users_list = list(referral_users.values("id", "email"))
            return Response(users_list, status=HTTP_200_OK)
        else:
            return Response({"message": "Приглашенных пользователей нет"}, status=HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Принимает набор учетных данных пользователя и возвращает пару токенов JSON "
                              "для доступа и обновления, чтобы подтвердить подлинность этих учетных данных.",
        operation_summary="Получение access/refresh JWT токена",
        tags=["Пользователь"],
        responses={
            200: openapi.Response(
                description="Токен успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access токен'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh токен'),
                    }
                )
            ),
            400: "Неверные учетные данные"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Принимает веб-токен JSON типа обновления и возвращает веб-токен JSON "
                              "типа доступа, если токен обновления действителен.",
        operation_summary="Получение access JWT токена",
        tags=["Пользователь"],
        responses={
            200: openapi.Response(
                description="Токен успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Новый Access токен'),
                    }
                )
            ),
            400: "Неверный Refresh токен"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)




