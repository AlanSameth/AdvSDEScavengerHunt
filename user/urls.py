from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page,name="Home"),
    path("logout/", views.logout_user),
    path("map/", views.Map,name="Map"),
    path("inputlocation/", views.input_location, name='input_location'),
    path("approval/", views.approval, name='approval'),
    path("your_location/", views.your_location, name='your_location'),
    path("first_page_game/", views.first_page_game, name='first_page_game'),
    path("<int:game_id>/input_game/", views.input_game, name='input_game'),
]