from django.db import models

from users.models import User


class Referral(models.Model):
    """Модель реферального кода"""

    code = models.CharField(
        max_length=6,
        verbose_name="Реферальный код",
    )
    validity_period = models.DateField(
        verbose_name="Срок действия реферального кода",
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
