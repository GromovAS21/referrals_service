from datetime import datetime
from rest_framework.exceptions import ValidationError

def validate_date_in_past(value: datetime.date) -> None:
    """Проверка на дату в прошлом"""

    if value < datetime.now().date():
        raise ValidationError("Дата не может быть в прошлом")
