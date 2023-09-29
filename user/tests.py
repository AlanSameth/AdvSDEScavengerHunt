from django.test import TestCase
from django.urls import reverse

from .models import User


# Create your tests here.
def create_User(name, email):
    """
    Create a User with the given `name` and 'email'.
    """
    return User.objects.create(user_name=name, user_email=email)


class UserModelTests(TestCase):
    def test_user_creation(self):
        """
        Test that User creation works.
        """
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email)
        self.assertIsInstance(User1, User)

class HomePageTests(TestCase):
    def test_home_page_exists(self):
        """
        Test that homepage is reachable.
        """
        url = reverse("home_page")
        response = self.client.get(url)
        self.assertContains(response, "home")