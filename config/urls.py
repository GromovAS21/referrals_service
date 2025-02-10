from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="users"),
    path("referral_codes/", include("referral_cods.urls"), name="referral_cods"),
]
