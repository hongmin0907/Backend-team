# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework import generics
# from rest_framework.permissions import AllowAny
#
# from stay.models import Stay
# from .serializers import StaySerializer
#
# class StaySearchList(generics.ListAPIView):
#     serializer_class = StaySerializer
#     permission_classes = (AllowAny,)
#
#     # def get_queryset(self):
#     #     queryset = Stay.objects.all()
#     #     searchKey = self.request.GET.get('searchKey')
#     #     queryset.filter(location__icontain=searchKey)
#     #     return queryset
#
# class SearchListAllApi(generics.ListAPIView):
#     queryset = Stay.objects.all()
#     serializer_class = StaySerializer
#     permission_classes = (AllowAny,)
#
#
# # from django.http import HttpResponse
# # from rest_framework.renderers import JSONRenderer
# #
# # class JSONResponse(HttpResponse):
# #     def __init__(self, data, **kwargs):
# #         content = JSONRenderer().render(data)
# #         kwargs['content_type'] = 'application/json'
# #         super(JSONResponse, self).__init__(content, **kwargs)
# #
# # def get_client_ip(request):
# #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# #     if x_forwarded_for:
# #         ip = x_forwarded_for.split(',')[0]
# #     else:
# #         ip = request.META.get('REMOTE_ADDR')
# #     ip_dic ={'ip':ip}
# #     return JSONResponse(ip_dic)
#
# class CurrentSearchList(generics.ListAPIView):
#     serializer_class = StaySerializer
#     permission_classes = (AllowAny,)
#
#     # def get_queryset(self):
#     #     queryset = Stay.objects.all()
#     #     # ip = get_client_ip(self.request)