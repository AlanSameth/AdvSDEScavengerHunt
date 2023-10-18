from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page),
    path("logout/", views.logout_user),
    path("map/", views.Map,name="Map"),
]