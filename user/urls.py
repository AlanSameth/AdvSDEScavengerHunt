from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page,name="Home"),
    path("logout/", views.logout_user),
    path("map/", views.Map,name="Map"),
    path("mapadmin/", views.map_admin, name='map_admin'),
]