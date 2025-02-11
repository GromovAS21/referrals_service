import datetime

from celery import shared_task

from referral_cods.models import Referral


@shared_task
def check_expiration_date_referral_code() -> None:
    """
    Проверка истекших сроков у реферальных кодов
    """

    date_today = datetime.date.today()
    # Находим реферальные коды которые меньше сегодняшней даты
    referral_codes = Referral.objects.filter(validity_period__lt=date_today, active=True)

    for code in referral_codes:
        code.active = False
        code.save(update_fields=["active"])