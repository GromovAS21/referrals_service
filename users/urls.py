from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateView, AllReferralUsersView

app_name = UsersConfig.name

urlpatterns =[
    # Токены
    path("api/token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

    path("", UserCreateView.as_view(permission_classes=(AllowAny,)), name="create_user"),
    path("referral_users/", AllReferralUsersView.as_view(), name="all_referral_users"),
]

