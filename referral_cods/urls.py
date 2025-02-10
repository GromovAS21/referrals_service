from django.urls import path

from referral_cods.apps import ReferralCodesConfig
from referral_cods.views import CreateReferralCodeView

app_name = ReferralCodesConfig.name

urlpatterns = [
    path("", CreateReferralCodeView.as_view(), name="create_referral_code"),
]