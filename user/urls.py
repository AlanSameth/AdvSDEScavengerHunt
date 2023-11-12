from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page,name="Home"),
    path("logout/", views.logout_user),
    path("inputlocation/logout/", views.logout_user),
    path("first_page_game/logout/", views.logout_user),
    path("<int:game_id>/map/logout/", views.logout_user),
    path("win/logout/", views.logout_user),
    path("choose_game/logout/", views.logout_user),
    path("approval/logout/", views.logout_user),
    path("your_game/logout/", views.logout_user, name='your_game'),
    path("<int:game_id>/map/", views.Map,name="Map"),
    path("inputlocation/", views.input_location, name='input_location'),
    path("approval/", views.approval, name='approval'),
    path("your_game/", views.your_game, name='your_game'),
    path("first_page_game/", views.first_page_game, name='first_page_game'),
    path("<int:game_id>/input_game/", views.input_game, name='input_game'),
    path("<int:game_id>/game_detail/", views.display_game_detail, name='display_game_detail'),
    path("choose_game/", views.choose_game, name='choose_game'),
    path("win/", views.win, name='win'),
]