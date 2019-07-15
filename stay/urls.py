from django.urls import path
from .views import *


app_name = "stay"

urlpatterns = [
    path("room/list/<int:stay_id>", room_list, name="room_list"),
    path("room/create/<int:stay_id>", room_create, name="room_create"),
    path("list/", stay_list, name="stay_list"),
    path("create/", stay_create, name="stay_create"),
    path("", main_page, name="main_page"),
]