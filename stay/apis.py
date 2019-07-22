from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import StaySerializer, RoomSerializer, CategorySerializer
from .models import *


# 숙소 리스트
class StayListApi(generics.ListAPIView):
    model = Stay.objects.all()
    serializer_class = StaySerializer
    # permission_classes = [AllowAny, ]


# 한 숙소 안에 모든 룸 리스트
class RoomListApi(generics.ListAPIView):
    model = Room.objects.all()
    serializer_class = RoomSerializer
    # permission_classes = [AllowAny, ]

# 카테고리 리스트
class CategoryListApi(generics.ListAPIView):
    model = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny, ]