from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):

        try:
            user = User.objects.create(
                email="admin@test.ru",
                is_staff=True,
                is_superuser=True,
            )
            user.set_password("Qwerty")
            user.save()
        except Exception:
            self.stdout.write(self.style.ERROR("SUPERUSER CREATE FAILED"))
        else:
            self.stdout.write(self.style.SUCCESS("SUPERUSER CREATE SUCCESS"))

