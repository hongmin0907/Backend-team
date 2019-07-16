from .models import Stay, Category, Room, Reservation
from rest_framework import serializers

class StaySerializer(serializers.ModelSerializer):
    model = Stay
    fields = '__all__'
class RoomSerializer(serializers.ModelSerializer):
    model = Room
    fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    models = Category
    fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
    models = Reservation
    fields = '__all__'