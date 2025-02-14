import os

import django
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):
        try:
            user = User.objects.create(
                email=os.getenv("ADMIN_EMAIL"),
                is_staff=True,
                is_superuser=True,
            )
            user.set_password(os.getenv("ADMIN_PASSWORD"))
            user.save()
        except django.db.utils.IntegrityError:
            self.stdout.write(self.style.ERROR("SUPERUSER ALREADY CREATED"))
        except Exception:
            self.stdout.write(self.style.ERROR("SUPERUSER CREATE FAILED"))
        else:
            self.stdout.write(self.style.SUCCESS("SUPERUSER CREATE SUCCESS"))
