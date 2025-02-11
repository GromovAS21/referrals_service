from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
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
        validators=[
            MinValueValidator(8, "Пароль должен содержать не менее 8 символов")
        ]
    )
    referral_users = models.ManyToManyField(
        "self",
        verbose_name="Приглашенные пользователи",
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("id",)