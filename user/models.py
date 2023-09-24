from django.db import models

# Create your models here.

class User(models.Model):
    """ this is the database for user information """
    user_name=models.CharField(max_length=400)
    user_email=models.CharField(max_length=400)
