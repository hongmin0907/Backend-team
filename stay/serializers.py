from .models import Stay, Category, Room, Reservation
from rest_framework import serializers
from .apis import mainPageApi

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = [
        "id",
        "name",
        "location",
        "builtDate",
        "remodeledDate",
        "introduce",
        "serviceKinds",
        "serviceIntroduce",
        "serviceNotice",
        "pickupNotice",
        "directions",
        "created",
        "updated",
        "category",
        ]

class MainSerializer(serializers.ModelSerializer):
    # stays = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name=mainPageApi.as_view()
    # )
    class Meta:
        model = Stay
        fields = ['keyword', 'stays']




class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'