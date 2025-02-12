import django
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание пользователя"""

    def handle(self, *args, **options):
        users = [
            {"email": "user_1@test.ru", "password": "Qwerty1", "referer_user_id": 1},
            {"email": "user_2@test.ru", "password": "Qwerty2", "referer_user_id": 1},
            {"email": "user_3@test.ru", "password": "Qwerty3"},
        ]

        users_for_create = []

        for user in users:
            users_for_create.append(User(**user))
            users_for_create[-1].set_password(user["password"])

        try:
            User.objects.bulk_create(users_for_create)
        except django.db.utils.IntegrityError:
            self.stdout.write(self.style.ERROR("USERS ALREADY CREATED"))
        except Exception:
            self.stdout.write(self.style.ERROR("USERS CREATE FAILED"))
        else:
            self.stdout.write(self.style.SUCCESS("USERS CREATE SUCCESS"))
