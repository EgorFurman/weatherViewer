from django.test import TestCase
from django.contrib.auth import get_user_model

from users.forms import UserRegistrationForm


User = get_user_model()


class UserRegistrationFormTest(TestCase):
    def test_valid_data(self):
        """Проверяем, что форма валидна с корректными данными"""
        form = UserRegistrationForm(
            data={
                'username': 'valid_user',
                'password1': 'ValidPass123!',
                'password2': 'ValidPass123!'
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_username_length(self):
        """Логин меньше минимальной длины"""
        form = UserRegistrationForm(
            data={
                'username': 'usr',  # меньше 4 символов
                'password1': 'ValidPass123!',
                'password2': 'ValidPass123!'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['Логин должен быть не короче 4 символов'])

    def test_duplicate_username(self):
        """Проверяем, что пароли должны совпадать"""
        User.objects.create_user(username='existing_user', password='ValidPass123!')

        form = UserRegistrationForm(
            data={
                'username': 'existing_user',
                'password1': 'ValidPass123!',
                'password2': 'ValidPass123!'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['Этот логин уже занят. Пожалуйста, выберите другой'])

    def test_password_dont_match(self):
        form = UserRegistrationForm(
            data={
                'username': 'new_user',
                'password1': 'ValidPass123!',
                'password2': 'MismatchPass123!'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['Пароли не совпадают'])

    def test_password_too_short(self):
        """Проверяем минимальную длину пароля"""
        form = UserRegistrationForm(
            data={
                'username': 'new_user',
                'password1': '123',
                'password2': '123'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertEqual(form.errors['password1'], ['Пароль должен быть не короче 6 символов'])

    def test_save_method(self):
        form = UserRegistrationForm(
            data={
                'username': 'new_user',
                'password1': 'ValidPass123!',
                'password2': 'ValidPass123!'
            }
        )

        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password('ValidPass123!'))  # Пароль должен быть хэширован
        self.assertEqual(user.username, 'new_user')