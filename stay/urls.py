from django.urls import path
from .views import *


app_name = "stay"

urlpatterns = [
    path("room/create/", room_create, name="room_create"),
    path("", stay_list, name="stay_list"),
]