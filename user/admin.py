

# Register your models here.
from django.contrib import admin

from .models import User, Game, location

admin.site.register(User)
admin.site.register(Game)
admin.site.register(location)