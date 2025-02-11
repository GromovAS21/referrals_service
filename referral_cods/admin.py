from django.contrib import admin

from referral_cods.models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Админка для модели Referral"""

    list_display = ("id", "code", "validity_period", "owner")
    list_filter = ("active", )
    search_fields = ("code",)
