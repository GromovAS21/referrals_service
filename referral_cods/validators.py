from datetime import date

from django.core.exceptions import ValidationError


class ValidateDateInPast:
    """Проверка на дату в прошлом"""

    def __call__(self, value):
        if value < date.today():
            raise ValidationError("Дата не может быть в прошлом")
