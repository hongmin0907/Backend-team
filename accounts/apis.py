from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .serializers import *
from config.permissions import *
# Create your views here.

class UserListView(generics.ListAPIView):
    """
    generics
    List : GET
    Create : POST
    Retrieve : GET
    Update : PUT, PATCH
    Destroy : Delete

    """
    # renderer_classes = [JSONRenderer] # 값만 보고 싶을때
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer

    filterset_fields = ('username', 'email')
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(pk=self.request.user.id)
        return queryset


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny, ]  # 회원가입 등의 뷰는 인증없이 작동해야하기 때문에 인증없이 사용해야 하는 뷰에 추가한다.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Your code
        user = serializer.save()
        token = Token.objects.create(user=user)

        # Create custom response
        data = serializer.data
        # You may need to serialize your token:
        # token = token.your_token_string_field
        data.update({'token': token})
        headers = self.get_success_headers(serializer.data)
        return HttpResponse(data, headers=headers)


class UserUpdateView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserModifySerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer


class UserDestroyView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDestroySerializer