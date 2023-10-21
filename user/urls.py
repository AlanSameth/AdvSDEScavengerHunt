from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page,name="Home"),
    path("logout/", views.logout_user),
    path("map/", views.Map,name="Map"),
    path("inputlocation/", views.input_location, name='input_location'),
]