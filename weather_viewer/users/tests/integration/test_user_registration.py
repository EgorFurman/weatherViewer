from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserRegistrationIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.registration_url = reverse('users:registration')
        cls.login_url = reverse('users:login')
        cls.home_url = reverse('home')
        cls.User = get_user_model()

        cls.username = 'new_user'
        cls.password = 'password1234!'

    def test_user_registration_flow(self):
        """
        Интеграционный тест полного процесса регистрации:
        1. Переход на страницу регистрации.
        2. Отправка валидной формы.
        3. Проверка редиректа и успешного создания пользователя.
        4. Авторизация пользователя после регистрации.
        """

        response = self.client.get(self.registration_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')

        registration_data = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
        }

        response = self.client.post(self.registration_url, data=registration_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(self.User.objects.filter(username='new_user').exists())

        login_data = {
            'username': self.username,
            'password': self.password,
        }

        response = self.client.post(self.login_url, data=login_data)

        user = self.User.objects.get(username=self.username)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(user.is_authenticated)

