from django.urls import path, include
from .views import *
from .apis import *

urlpatterns_api = [
    path('list/', UserListView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('update/<int:pk>/', UserUpdateView.as_view()),
    path('detail/<int:pk>/', UserDetailView.as_view()),
    path('delete/<int:pk>/', UserDestroyView.as_view()),
]

urlpatterns = [
    path('api/', include(urlpatterns_api)),
]