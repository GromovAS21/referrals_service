from datetime import datetime
from rest_framework.exceptions import ValidationError
from referral_cods.models import Referral


class ActiveReferralCodeValidator:
    """Проверка на имеющиеся реферального кода"""

    def __init__(self, owner):
        self.owner = owner

    def __call__(self):
        if Referral.objects.filter(owner=self.owner, active=True).exists():
            raise ValidationError("Вы уже имеете активный реферальный код, для создания нового кода необходимо удалить имеющийся код.")


def validate_date_in_past(value: datetime.date) -> None:
    """Проверка на дату в прошлом"""

    if value < datetime.now().date():
        raise ValidationError("Дата не может быть в прошлом")
