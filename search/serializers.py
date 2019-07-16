from rest_framework import serializers

from .models import Search, Stay

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['searchKey', 'stays']

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'