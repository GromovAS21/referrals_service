import requests

from config.settings import HUNTER_API_KEY


def verify_email(email: str) -> bool:
    """Проверка email на валидность через сайт Hunter.io"""

    api_key = HUNTER_API_KEY
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

    response = requests.get(url).json()

    try:
        status = response["data"]["status"]
    except KeyError:
        return False

    else:
        if not status == "invalid":
            return True
        return False
