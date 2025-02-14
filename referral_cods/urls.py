from django.urls import path

from referral_cods.apps import ReferralCodesConfig
from referral_cods.views import (
    CreateReferralCodeView,
    DeleteReferralCodeView,
    SendEmailReferralCodeView,
)

app_name = ReferralCodesConfig.name

urlpatterns = [
    path("", CreateReferralCodeView.as_view(), name="create_referral_code"),
    path("<int:pk>/", DeleteReferralCodeView.as_view(), name="delete_referral_code"),
    path("send_code/", SendEmailReferralCodeView.as_view(), name="send_referral_code"),
]
