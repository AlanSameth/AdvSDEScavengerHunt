from django.db import models

# Create your models here.

class User(models.Model):
    """ this is the database for user information """
    user_name=models.CharField(max_length=400)
    user_email=models.CharField(max_length=400)
    is_admin=models.BooleanField(default=False)

class Game(models.Model):
    game_description = models.CharField(max_length=400, null=True)
    game_name = models.CharField(max_length=400)

class location(models.Model):
    """ this is the database for Hidden location information """
    zipcode = models.CharField(max_length=400)
    city = models.CharField(max_length=400)
    country = models.CharField(max_length=400)
    address = models.CharField(max_length=400,blank=True,null=True)
    last_edited_time = models.DateTimeField(auto_now=True,null=True)
    latitude = models.CharField(max_length=400,blank=True,null=True)
    longitude = models.CharField(max_length=400,blank=True,null=True)
    place_id = models.CharField(max_length=400,blank=True,null=True)
    hint = models.CharField(max_length=400, null=True)
    clue = models.CharField(max_length=400, null=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)
