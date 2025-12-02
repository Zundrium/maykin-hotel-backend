from rest_framework import viewsets
from .models import City, Hotel
from .serializers import CitySerializer, HotelSerializer

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.all().order_by('name')
    serializer_class = HotelSerializer
    filterset_fields = ['city', 'city__code']
