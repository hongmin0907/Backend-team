from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .models import Search, Stay
from .serializers import SearchSerializer, StaySerializer

# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

# @api_view(['GET'])
# def searchList(request):
#     receive_from_client = {
#         'searchKey': '역삼',
#     }
#     if request.method == 'GET':
#         # Search 모델에서 searchKey 필드와 receive_from_client['searchKey'] 조인해서 가져온 쿼리셋 입니다
#         search = Search.objects.filter(searchKey=receive_from_client['searchKey'])
#         print(search)
#         # 이렇게 하면 캐시에 전체 쿼리셋이 저장되지않고 레코드 하나가 존재하는지 알려준다
#         if search.exists():
#             stay = search.get()
#             # Search 모델 안에 ManyToManyFields로 Stay모델을 참조하여 가지고 있으며 참조된 데이타들을 모두 불러내서 시리얼라이즈 하려고 하는 것입니다
#             serializer = StaySerializer(data=stay.stays.all(), many=True)
#             # return Response(serializer.data)
#
#             # serializer.is_valid()가 계속 else로 빠집니다
#             if serializer.is_valid():
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.data)
#                 # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         else:
#             if Search.objects.filter(searchKey=receive_from_client['searchKey']):
#                 search = Search.objects.filter(searchKey=receive_from_client['searchKey'])
#             else:
#                 search = Search()
#                 search.searchKey = receive_from_client['searchKey']
#                 search.save()
#                 stays = Stay.objects.filter(searchTag=receive_from_client['searchKey'])
#                 for stay in stays:
#                     search.stays.add(stay)
#                 serializer = StaySerializer(data=stays, many=True)
#                 if serializer.is_valid():
#                     return Response(serializer.data)
#                 else:
#                     return Response(serializer.data)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchList(APIView):
    def get(self, request, *args, **kwargs):
        receive_from_client = {
            'searchKey': '역삼',
        }
        search = Search.objects.filter(searchKey=receive_from_client['searchKey'])
        if search.exists():
            stay = search.get()
            serializer = StaySerializer(stay.stays.all(), many=True)
            print(serializer.data)
            return Response(serializer.data)
        else:
            serializer = SearchSerializer(data=receive_from_client)
            if serializer.is_valid():
                stays = Stay.objects.filter(searchTag=receive_from_client['searchKey'])
                for stay in stays:
                    serializer.instance.stays.add(stay)
                serializer.save()
                if stays:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.POST.get('searchKey')
        print(data)
        search = Search.objects.filter(searchKey=data)

        stay = search.get()
        serializer = StaySerializer(stay.stays.all(), many=True)
        print(serializer.data)
        return Response(serializer.data)