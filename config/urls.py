from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Реферальный сервис",
      default_version="v1",
      description="Pet-проект для создания реферальных кодов и возможностью регистрироваться при вводе действующего реферального кода",
      contact=openapi.Contact(email="GromovAS121@yandex.ru"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="users"),
    path("referral_codes/", include("referral_cods.urls"), name="referral_cods"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

