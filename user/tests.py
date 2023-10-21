from unittest import mock

from django.test import TestCase
from django.urls import reverse

from .models import User


# Create your tests here.

def create_User(name, email, is_admin):
    """
    Create a User with the given `name` and 'email' and admin status.
    """
    return User.objects.create(user_name=name, user_email=email, is_admin=is_admin)


class UserModelTests(TestCase):
    def test_user_creation(self):
        """
        Test that User creation works.
        """
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email, False)
        self.assertIsInstance(User1, User)

    def test_admin_creation(self):
        """
        Test that Admin creation works.
        """
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email, True)
        self.assertTrue(User1.is_admin)

class HomePageTests(TestCase):
    def test_home_page_exists(self):
        """
        Test that created User will be treated as a User.
        """
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email, False)
        User1.save()
        self.assertIn(User1, User.objects.all())

    def test_admin_page_exists(self):
        """
        Test that created Admin will be treated as an Admin.
        """
        name = "dummy"
        email = "User@virginia.edu"
        Admin1 = create_User(name, email, True)
        Admin1.save()
        self.assertIn(Admin1, User.objects.all().filter(is_admin = True))
