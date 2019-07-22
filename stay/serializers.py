from .models import Stay, Category, Room, Reservation
from rest_framework import serializers

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'

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