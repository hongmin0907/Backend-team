from django.urls import path
from .views import *


app_name = "stay"

urlpatterns = [
    path("create/", stay_create, name="stay_create"),
    path("", stay_list, name="stay_list"),
]