from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='root', password='root')
        # Создаем тестового пользователя
        self.login_url = reverse('users:user-login')  # URL для получения JWT-токенов (замените на ваш)
        self.protected_url = reverse('books:protected_view')  # URL защищенного эндпоинта (замените на ваш)

    def test_obtain_jwt_token(self):
        """Тест успешного получения JWT-токена"""
        data = {'username': 'root', 'password': 'root'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Проверяем, что вернулся access-токен
        self.assertIn('refresh', response.data)  # Проверяем, что вернулся refresh-токен

    def test_protected_endpoint_without_token(self):
        """Тест доступа к защищенному эндпоинту без токена"""
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_protected_endpoint_with_valid_token(self):
        """Тест доступа к защищенному эндпоинту с валидным токеном"""
        # Генерируем токен вручную для тестового пользователя
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Добавляем токен в заголовок
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoint_with_invalid_token(self):
        """Тест доступа к защищенному эндпоинту с невалидным токеном"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
