from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    password = models.CharField(
        max_length=128,
        verbose_name="Пароль",
    )
    referer_user = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="пользователь который пригласил данного пользователя",
        blank=True,
        null=True,
        related_name="referral_users"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("id",)
