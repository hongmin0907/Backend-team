from django.urls import path
from .views import *


urlpatterns = [
    path('list/', UserListView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('update/<int:pk>/', UserUpdateView.as_view()),
    path('detail/<int:pk>/', UserDetailView.as_view()),
    path('delete/<int:pk>/', UserDestroyView.as_view()),
]