from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'cities', viewsets.CityViewSet)
router.register(r'hotels', viewsets.HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
