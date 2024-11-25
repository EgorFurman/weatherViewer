from django.test import TestCase
from django.contrib.auth import get_user_model

from users.forms import UserAuthorizationForm


class UserAuthorizationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123!"
        )

    def test_valid_credentials(self):
        """Проверяем авторизацию с корректными данными"""
        form = UserAuthorizationForm(
            data={
                'username': 'testuser',
                'password': 'testpassword123!'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_invalid_username(self):
        """Проверяем, что неверное имя пользователя вызывает ошибку"""
        form = UserAuthorizationForm(
            data={
                'username': 'wrong_user',
                'password': 'testpassword123!'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'], ['Неверный логин или пароль'])

    def test_invalid_password(self):
        """Проверяем, что неверный пароль вызывает ошибку"""
        form = UserAuthorizationForm(
            data={
                'username': 'testuser',
                'password': 'WrongPass123!'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'], ['Неверный логин или пароль'])

    def test_empty_username(self):
        """Проверяем валидацию пустого логина"""
        form = UserAuthorizationForm(
            data={
                'username': '',
                'password': 'ValidPass123!'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['Обязательное поле.'])

    def test_empty_password(self):
        """Проверяем валидацию пустого пароля"""
        form = UserAuthorizationForm(data={
            'username': 'testuser',
            'password': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'], ['Обязательное поле.'])
