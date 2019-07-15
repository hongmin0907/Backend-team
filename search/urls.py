from django.urls import path
from . import apis

urlpatterns = [
    path('test/', apis.SearchList.as_view()),
]