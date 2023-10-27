import datetime
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from .models import User, location, Game
from .views import home_page


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

    def test_user_exists(self):
        """
        Test that created User will be treated as a User.
        """
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email, False)
        User1.save()
        self.assertIn(User1, User.objects.all())

    def test_admin_exists(self):
        """
        Test that created Admin will be treated as an Admin.
        """
        name = "dummy"
        email = "User@virginia.edu"
        Admin1 = create_User(name, email, True)
        Admin1.save()
        self.assertIn(Admin1, User.objects.all().filter(is_admin=True))


class MapTests(TestCase):
    def test_location_creation(self):
        q = location.objects.create(zipcode=12345, city='town', country='America', address= '180 road street', last_edited_time= datetime.time, latitude=0, longitude=0, place_id=1)
        self.assertIsInstance(q, location)

    def test_location_exists(self):
        q = location.objects.create(zipcode=12345, city='town', country='America', address= '180 road street', last_edited_time= datetime.time, latitude=0, longitude=0, place_id=1)
        q.save()
        self.assertIn(q, location.objects.all())

class SubmissionTests(TestCase):
    def test_create_game(self):
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email, False)
        User1.save()
        Game1 = Game.objects.create(user_id=User1, game_name="game")
        Game1.save()
        self.assertIn(Game1, Game.objects.all())

    def test_create_location_for_game(self):
        name = "dummy"
        email = "User@virginia.edu"
        User1 = create_User(name, email, False)
        User1.save()
        Game1 = Game.objects.create(user_id=User1, game_name="game")
        Game1.save()
        location1 = location.objects.create(zipcode="1", city="home", country="USA", address="1234 road street", hint= "turn around", game_id=Game1)
        location1.save()
        self.assertIn(location1, location.objects.all())