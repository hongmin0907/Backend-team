from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

# 숙소 리스트
class StayListApi(APIView):
    def get(self, request, *args, **kwargs):
        stays = Stay.objects.all()
        serializer = serializers(stays, many=True)
        return Response(serializer.data)
# 한 숙소 안에 모든 룸 리스트
class RoomListApi(APIView):
    def post(self, request, *args, **kwargs):
        stay = request.POST.get('stayId')
        rooms = Room.objects.filter(stay=stay)
        serializer = serializers(rooms, many=True)
        return Response(serializers.data)
# 카테고리 리스트
class CategoryListApi(APIView):
    def get(self, request, *args, **kwargs):
        category = Category.obejcts.all()
        serializer = serializers(category, many=True)
        return Response(serializers.data)