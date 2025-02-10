from django.contrib import admin

from referrals.models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Админка для модели Referral"""

    list_display = ("id", "code", "validity_period", "owner")
    list_filter = ("owner",)
    search_fields = ("code",)

