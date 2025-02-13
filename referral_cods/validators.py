from datetime import date, datetime

from django.core.exceptions import ValidationError


def validate_date_in_past(value: datetime) -> None:
    """Проверка на дату в прошлом"""

    date_input = value

    # Проверка являются ли тип данных date, или это строка вводимая в админ панели
    if not isinstance(date_input, date):
        date_input = datetime.strftime(value, "%Y-%m-%d").date()

    if date_input < date.today():
        raise ValidationError("Дата не может быть в прошлом")
