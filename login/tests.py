from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

class LoginViewTest(TestCase):

    def test_valid_request(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_valid_login(self):
        User.objects.create_user("ronan", password="pw")
        response = self.client.post(reverse("login"),
                                    {"username": "ronan",
                                     "password": "pw"})
        self.assertRedirects(response, reverse("todo"))

    def test_valid_login(self):
        """
        Check if we didn't successfully log in. We would have gotten a
        re-direct, and so a 302 instead of 200.
        """
        User.objects.create_user("ronan", password="pw")
        response = self.client.post(reverse("login"),
                                    {"username": "ronan",
                                     "password": "incorrect_pw"})
        self.assertEqual(200, response.status_code)

class RegisterViewTest(TestCase):

    def test_valid_request(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "auth/register.html")

class LogoutViewTest(TestCase):

    def test_valid_request(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
