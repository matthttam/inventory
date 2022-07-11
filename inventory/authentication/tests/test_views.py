from django.test import TestCase
from django.urls import reverse
from django.contrib import auth

from .factories import UserFactory


class LoginViewTest(TestCase):
    def test_login_page(self):
        response = self.client.get(reverse("authentication:login"))
        self.assertEqual(response.status_code, 200)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_login_page_with_valid_credentials(self):
        username = "test_username"
        password = "test_password123!"
        user = UserFactory(username=username, password=password)
        response = self.client.post(
            reverse("authentication:login"),
            {"username": username, "password": password},
        )
        self.assertRedirects(response, "/", status_code=302)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_login_page_with_invalid_credentials(self):
        username = "test_username"
        wrong_password = "wrong_password"
        user = UserFactory(username=username, password="test_password123!")
        response = self.client.post(
            reverse("authentication:login"),
            {"username": username, "password": wrong_password},
        )
        self.assertContains(
            response, "Your username and password didn't match. Please try again."
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class LoggedOutViewTest(TestCase):
    def logged_out_redirect(self):
        pass
