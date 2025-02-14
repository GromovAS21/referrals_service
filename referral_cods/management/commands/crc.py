from django.core.management import BaseCommand

from referral_cods.models import ReferralCode


class Command(BaseCommand):
    """Создание реферального кода"""

    def handle(self, *args, **options):
        referral_codes = [
            {
                "code": "111111",
                "validity_period": "2025-12-12",
                "active": True,
                "owner_id": 1,
            },
            {
                "code": "222222",
                "validity_period": "2025-12-12",
                "active": True,
                "owner_id": 2,
            },
            {
                "code": "333333",
                "validity_period": "2025-12-12",
                "active": False,
                "owner_id": 3,
            },
        ]

        referral_codes_for_create = []

        for code in referral_codes:
            referral_codes_for_create.append(ReferralCode(**code))

        ReferralCode.objects.bulk_create(referral_codes_for_create)
        self.stdout.write(self.style.SUCCESS("REFERRAL CODES CREATE SUCCESS"))
