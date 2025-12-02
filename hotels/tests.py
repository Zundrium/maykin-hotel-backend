from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from .models import City, Hotel
import io

class ModelTests(TestCase):
    def test_city_creation(self):
        city = City.objects.create(code='AMS', name='Amsterdam')
        self.assertEqual(str(city), 'Amsterdam')
        self.assertEqual(city.code, 'AMS')

    def test_hotel_creation(self):
        city = City.objects.create(code='AMS', name='Amsterdam')
        hotel = Hotel.objects.create(city=city, zone='Z1', name='Hotel A')
        self.assertEqual(str(hotel), 'Hotel A')
        self.assertEqual(hotel.city, city)

class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(code='AMS', name='Amsterdam')
        self.hotel = Hotel.objects.create(city=self.city, zone='Z1', name='Hotel A')

    def test_city_list_api(self):
        response = self.client.get(reverse('city-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Amsterdam')

    def test_hotel_list_api(self):
        response = self.client.get(reverse('hotel-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Hotel A')

    def test_hotel_filter_api(self):
        response = self.client.get(reverse('hotel-list') + '?city=AMS')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        response = self.client.get(reverse('hotel-list') + '?city=XYZ')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

class ImportCommandTests(TestCase):
    @patch('hotels.management.commands.import_hotel_data.requests.get')
    def test_import_command(self, mock_get):
        # Mock responses
        mock_city_response = MagicMock()
        mock_city_response.status_code = 200
        mock_city_response.text = 'AMS;Amsterdam\nROT;Rotterdam'
        
        mock_hotel_response = MagicMock()
        mock_hotel_response.status_code = 200
        mock_hotel_response.text = 'AMS;Z1;Hotel A\nROT;Z2;Hotel B'

        # Configure side_effect to return different responses for different calls
        # Note: The command calls requests.get twice.
        # We need to ensure the order or check URL.
        # Simpler: just return based on call order if we know it.
        # But better to check args.
        
        def side_effect(url, auth, timeout):
            if 'city.csv' in url:
                return mock_city_response
            elif 'hotel.csv' in url:
                return mock_hotel_response
            return MagicMock(status_code=404)

        mock_get.side_effect = side_effect

        out = io.StringIO()
        call_command('import_hotel_data', stdout=out)
        
        self.assertIn('Cities: 2 created, 0 updated, 0 skipped', out.getvalue())
        self.assertIn('Hotels: 2 created, 0 updated, 0 skipped, 0 warnings', out.getvalue())

        self.assertEqual(City.objects.count(), 2)
        self.assertEqual(Hotel.objects.count(), 2)
        self.assertTrue(Hotel.objects.filter(name='Hotel A').exists())

        # Test update scenario
        # Run command again with modified data to test updates and skips
        mock_city_response.text = 'AMS;Amsterdam Updated\nROT;Rotterdam' # AMS updated, ROT skipped
        mock_hotel_response.text = 'AMS;Z1;Hotel A\nROT;Z2;Hotel B Updated' # Hotel A skipped, Hotel B updated
        
        # Reset mock side effect to return these new responses (or just reuse if they are mutable objects)
        # Since we defined side_effect using the objects, modifying the objects works if we didn't recreate them inside side_effect.
        # But side_effect was a function returning these objects.
        
        out_update = io.StringIO()
        call_command('import_hotel_data', stdout=out_update)
        
        self.assertIn('Cities: 0 created, 1 updated, 1 skipped', out_update.getvalue())
        self.assertIn('Hotels: 0 created, 1 updated, 1 skipped, 0 warnings', out_update.getvalue())
        
        self.assertEqual(City.objects.get(code='AMS').name, 'Amsterdam Updated')
        self.assertEqual(Hotel.objects.get(city__code='ROT', zone='Z2').name, 'Hotel B Updated')
