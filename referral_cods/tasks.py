import datetime

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from referral_cods.models import ReferralCode


@shared_task
def check_expiration_date_referral_code() -> None:
    """
    Проверка истекших сроков у реферальных кодов
    """

    date_today = datetime.date.today()
    # Находим реферальные коды которые меньше сегодняшней даты
    referral_codes = ReferralCode.objects.filter(validity_period__lt=date_today, active=True)

    for code in referral_codes:
        code.active = False
        code.save(update_fields=["active"])


@shared_task
def send_referral_code_email(referral_code_data: dict, user_email: str) -> None:
    """Отправка реферального кода на email"""

    referral_code = referral_code_data["code"]
    validity_period = referral_code_data["validity_period"]
    formatted_date = validity_period.strftime("%d %m %Y")
    user_email = user_email

    send_mail(
        subject="Реферальный код",
        message=f"Твой реферальный код: {referral_code}.\n" f"Код активен до: {formatted_date} года.",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
