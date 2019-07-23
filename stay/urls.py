from django.urls import path, include
from .views import *
from .apis import *

app_name = "stay"

urlpatterns_apis = [
    path('category/', CategoryListApi.as_view()),
    path('stay/', StayListApi.as_view()),
    path('room/', RoomListApi.as_view()),
    path('testcategory/', MainSearchListApi.as_view()),
    path('testmain/', mainPageApi.as_view()),
]

urlpatterns = [
    path("room/list/<int:stay_id>", room_list, name="room_list"),
    path("room/create/<int:stay_id>", room_create, name="room_create"),
    path("list/", stay_list, name="stay_list"),
    path("create/", stay_create, name="stay_create"),
    path("", main_page, name="main_page"),
    path('api/', include(urlpatterns_apis)),
]