from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserAuthorizationViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:login')
        User.objects.create_user(username='test_user', password='password123?').save()

    def test_page_available(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_successful_login(self):
        response = self.client.post(self.url, {'username': 'test_user', 'password': 'password123?'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_invalid_username(self):
        response = self.client.post(self.url, {'username': 'wrong_user', 'password': 'password123?'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_invalid_password(self):
        response = self.client.post(self.url, {'username': 'test_user', 'password': 'wrong_password123?'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

