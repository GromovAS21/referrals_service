from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from referral_cods.models import ReferralCode
from users.models import User


class ReferralCodeTest(TestCase):
    """Тест для модели ReferralCode"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.ru")
        self.user_1 = User.objects.create(
            email="test1@test.ru",
        )
        self.referral_code = ReferralCode.objects.create(
            code=123456, validity_period="2026-01-01", active=False, owner=self.user
        )

    def test_referral_code(self):
        """Тест модели ReferralCode"""
        self.assertEqual(self.referral_code.code, 123456)
        self.assertEqual(self.referral_code.validity_period, "2026-01-01")
        self.assertEqual(self.referral_code.active, False)
        self.assertEqual(self.referral_code.owner, self.user)

    def test_create_referral_code(self):
        """Тест создания реферального кода"""

        data = {
            "code": "123456",
            "validity_period": "2026-01-01",
        }
        url = reverse("referral_cods:create_referral_code")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ReferralCode.objects.filter(code="123456").exists())

        data = {
            "code": "12345",
            "validity_period": "2025-01-01",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["code"][0], "Код должен состоять из 6 цифр")
        self.assertEqual(response.json()["validity_period"][0], "Дата не может быть в прошлом")

    def test_delete_referral_code(self):
        """Тест на удаление реферального когда"""

        url = reverse("referral_cods:delete_referral_code", args=(self.referral_code.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_send_referral_code(self):
        """Тест на отправку кода на Email"""

        url = reverse("referral_cods:send_referral_code")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Активный реферальный код отсутствует")

        ReferralCode.objects.create(code=123456, validity_period="2026-01-01", active=True, owner=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Сообщение отправлено на Ваш Email")
