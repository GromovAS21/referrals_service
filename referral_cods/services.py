from typing import Optional

from django.core.cache import cache

from referral_cods.models import ReferralCode
from users.models import User


class ReferralCodeService:
    """Реферальный код"""

    @staticmethod
    def get_referral_code_data(user: User) -> Optional[dict]:
        """Проверка наличия активного кода"""
        # Проверка хэша на наличии реферального кода
        referral_code = cache.get(f"referral_code_{user.pk}")
        validity_period = cache.get(f"validity_period_{user.pk}")

        if not referral_code and not validity_period:
            try:
                referral_code_obj = ReferralCode.objects.get(owner=user, active=True)
                referral_code = referral_code_obj.code
                validity_period = referral_code_obj.validity_period
            except ReferralCode.DoesNotExist:
                return None
        # Создание словаря с данными реферального кода
        return {
            "code": referral_code,
            "validity_period": validity_period
        }

    @staticmethod
    def get_user_email(user:User) -> str:
        return user.email