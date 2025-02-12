from django.contrib import admin

from referral_cods.models import ReferralCode


@admin.register(ReferralCode)
class ReferralAdmin(admin.ModelAdmin):
    """Админка для модели ReferralCode"""

    list_display = ("id", "code", "validity_period", "owner")
    list_filter = ("active", )
    search_fields = ("code",)
