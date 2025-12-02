from rest_framework import serializers
from .models import City, Hotel

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','code', 'name']

class HotelSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'city', 'city_name', 'zone', 'name']
