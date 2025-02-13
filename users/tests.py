from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from referral_cods.models import ReferralCode
from users.models import User


class UserTest(TestCase):
    """Тест для модели User"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.ru",
        )
        self.user_1 = User.objects.create(
            email="test1@test.ru",
            referer_user=self.user,
        )
        self.user_2 = User.objects.create(
            email="test2@test.ru",
            referer_user=self.user,
        )
        self.referral_code = ReferralCode.objects.create(
            code=123456, validity_period="2026-01-01", active=True, owner=self.user
        )

    def test_user(self):
        """Тест модели пользователя"""

        self.assertEqual(self.user.email, "test@test.ru")
        self.assertEqual(self.user_1.referer_user, self.user)

    def test_create_user(self):
        """Тест на создание пользователя"""

        url = reverse("users:create_user")
        data = {
            "email": "test@example.com",
            "password": "Qwerty123",
            "referral_code": self.referral_code.code,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Тест на корректный пароль
        data = {
            "email": "test1@example.com",
            "password": "Qwerty",
            "referral_code": self.referral_code.code,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["password"][0],
            "Убедитесь, что это значение содержит не менее 8 символов.",
        )

        # Тест на активный реферальный код
        data = {
            "email": "test2@example.com",
            "password": "Qwerty123",
            "referral_code": "123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["referral_code"], "Такого реферального кода не существует"
        )

    def test_all_referral_users(self):
        """Тест на список реферальных пользователей текущего пользователя"""

        url = reverse("users:all_referral_users")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
