from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import StaySerializer, RoomSerializer, CategorySerializer, MainSerializer
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

class MainSearchListApi(generics.ListAPIView):
    serializer_class = StaySerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        searchKey=self.request.GET.get('searchKey')
        if searchKey:
            category = Category.objects.get(staying=searchKey)
            queryset = Stay.objects.filter(category=category)
            return queryset
        else:
            category = Category.objects.get(staying='펜션')
            queryset = Stay.objects.filter(category=category)
            return queryset

class MainListApi(generics.ListAPIView):
    serializer_class = StaySerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        searchKey = []
        searchKey.append('초특가')
        searchKey.append('수영장')

# class mainPageApi(generics.ListAPIView):
#     queryset = Stay.objects.all()
#     serializer_class = StaySerializer
#     permission_classes = [AllowAny, ]
#
#
#     def get_serializer_context(self):
#         context = super(mainPageApi, self).get_serializer_context()
#         queryset = super().get_queryset()
#         # stays = Stay.objects.all()
#         bigSaleStays = queryset.filter(keywords__name__in=["초특가"])
#         swimmingStays = queryset.filter(keywords__name__in=["수영장"])
#         partyStays = queryset.filter(keywords__name__in=["파티룸"])
#         context.update({
#             'bigSaleStays': bigSaleStays,
#             'swimmingStays': swimmingStays,
#             'partyStays': partyStays,
#         })
#         print(context['swimmingStays'])
#         return context
#
#     def get_serializer(self, *args, **kwargs):
#         """
#         Return the serializer instance that should be used for validating and
#         deserializing input, and for serializing output.
#         """
#         serializer_class = self.get_serializer_class()
#         kwargs['context'] = self.get_serializer_context()
#         # print(kwargs['context']['bigSaleStays'])
#         return serializer_class(*args, **kwargs)

class mainPageApi(generics.ListAPIView):
    queryset = Stay.objects.all()
    serializer_class = MainSerializer
    permission_classes = [AllowAny, ]


    def get_serializer_context(self):
        context = super(mainPageApi, self).get_serializer_context()
        queryset = super().get_queryset()
        # stays = Stay.objects.all()
        bigSaleStays = queryset.filter(keywords__name__in=["초특가"])
        swimmingStays = queryset.filter(keywords__name__in=["수영장"])
        partyStays = queryset.filter(keywords__name__in=["파티룸"])
        context.update({
            'bigSaleStays': bigSaleStays,
            'swimmingStays': swimmingStays,
            'partyStays': partyStays,
        })
        print(context['swimmingStays'])
        return context

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        # print(kwargs['context']['bigSaleStays'])
        return serializer_class(*args, **kwargs)
