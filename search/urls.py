from django.urls import path, include
from . import apis

urlpatterns_api = [
    path('test/', apis.SearchListApi.as_view()),
]

urlpatterns = [
    path('api/', include(urlpatterns_api)),
]