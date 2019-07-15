from rest_framework import serializers

from .models import User


# 유저 목록에 출력될 형식
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# 회원 가입할 때 필요한 필드들에 관한 시리얼라이저
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        return user

# 유저 정보 수정 할 때 나타낼 데이터 필드
class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name', 'email', 'phoneNumber']

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password' and value:
                instance.set_password(value)
            elif value:
                setattr(instance, key, value)
        instance.save()
        return instance

# 유저 정보에 나타낼 필드
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',  'first_name', 'last_name', 'email', 'phoneNumber']

# 유저 삭제
class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']