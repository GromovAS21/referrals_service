from django.urls import path

from users.apps import UsersConfig
from users.views import AllReferralUsersView, CustomTokenObtainPairView, CustomTokenRefreshView, UserCreateView


app_name = UsersConfig.name

urlpatterns = [
    # Токены
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("", UserCreateView.as_view(), name="create_user"),
    path("referral_users/", AllReferralUsersView.as_view(), name="all_referral_users"),
]
