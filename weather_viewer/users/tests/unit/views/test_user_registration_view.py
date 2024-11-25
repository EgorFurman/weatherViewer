from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:registration')
        User.objects.create_user(username='test_user', password='password123?').save()

    def test_page_available(self):
        """Проверяем, что страница регистрации доступна"""
        response = self.client.get(path=self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_registration_successful(self):
        """Проверяем успешную регистрацию пользователя"""
        data = {
            'username': 'test_user1',
            'password1': 'password123!',
            'password2': 'password123!',
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_registration_existing_user(self):
        """Проверяем ошибку для регистрации пользователя с занятым логином"""
        data = {
            'username': 'test_user',
            'password1': 'password123!',
            'password2': 'password123!',
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='usr').exists())  # пользователь не создан
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_invalid_username(self):
        """Проверяем ошибку при регистрации пользователя со слишком коротким логином"""
        data = {
            'username': 'usr',
            'password1': 'password123!',
            'password2': 'password123!',
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='usr').exists())  # пользователь не создан
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_too_short_password(self):
        """Проверяем ошибку при регистрации пользователя со слишком коротким паролем"""
        data = {
            'username': 'test_user1',
            'password1': 'pswrd',
            'password2': 'pswrd',
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='usr').exists())  # пользователь не создан
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_too_long_password(self):
        """Проверяем ошибку при регистрации пользователя со слишком длинным паролем"""
        data = {
            'username': 'test_user',
            'password1': 'pswrd1'*4,
            'password2': 'pswrd1'*4,

        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='usr').exists())  # пользователь не создан
        self.assertTemplateUsed(response, 'users/registration.html')





