from django.core.validators import RegexValidator
from django.db import models

from referrals.validators import validate_date_in_past
from users.models import User


class Referral(models.Model):
    """Модель реферального кода"""

    code = models.CharField(
        max_length=6,
        verbose_name="Реферальный код",
        validators=[
            RegexValidator(r"^\d{6}$", "Код должен состоять из цифр"),
        ]
    )
    validity_period = models.DateField(
        verbose_name="Срок действия реферального кода",
        validators=[
            RegexValidator(r"^\d{4}-\d{2}-\d{2}$", "Дата должна быть в формате ГГГГ-ММ-ДД"),
            validate_date_in_past
        ]
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Активность реферального кода",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец реферального кода",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Реферальный код"
        verbose_name_plural = "Реферальные коды"
        ordering = ("id",)
