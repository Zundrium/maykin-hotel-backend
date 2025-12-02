import csv
import io
import os
import logging
import requests
from django.core.management.base import BaseCommand, CommandError
from requests.auth import HTTPBasicAuth
from hotels.models import City, Hotel

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports City and Hotel data from remote CSV files using .env credentials'

    MAYKIN_API_ENDPOINT = os.getenv('MAYKIN_API_ENDPOINT')
    CITY_CSV_URL = f'{MAYKIN_API_ENDPOINT}/city.csv'
    HOTEL_CSV_URL = f'{MAYKIN_API_ENDPOINT}/hotel.csv'

    def handle(self, *args, **options):
        # 1. Haal credentials op uit environment variables (.env)
        api_user = os.getenv('MAYKIN_API_USER')
        api_pass = os.getenv('MAYKIN_API_PASS')

        if not api_user or not api_pass:
            raise CommandError(
                "Credentials missing! Please set MAYKIN_API_USER and "
                "MAYKIN_API_PASS in your .env file."
            )

        self.auth = HTTPBasicAuth(api_user, api_pass)

        self.stdout.write("Starting import...")

        # 2. Import Cities
        cities_rows = self._fetch_csv_datarows(self.CITY_CSV_URL)
        if cities_rows:
            self._process_cities(cities_rows)
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch cities. Aborting."))
            return

        # 3. Import Hotels
        hotels_rows = self._fetch_csv_datarows(self.HOTEL_CSV_URL)
        if hotels_rows:
            self._process_hotels(hotels_rows)

        self.stdout.write(self.style.SUCCESS("Import process finished."))

    def _fetch_csv_datarows(self, url):
        try:
            response = requests.get(url, auth=self.auth, timeout=30)
            response.raise_for_status()

            # Decode content to string if needed, though response.text handles charset usually
            f = io.StringIO(response.text)
            # CSV delimiter is puntkomma, geen headers
            reader = csv.reader(f, delimiter=';')
            return list(reader)

        except requests.RequestException as e:
            logger.error(f"Network error fetching {url}: {e}")
            self.stderr.write(self.style.ERROR(f"Network error fetching {url}: {e}"))
            return None

    def _process_cities(self, rows):
        stats = {'created': 0, 'updated': 0, 'skipped': 0}
        
        for row in rows:
            if len(row) < 2: continue
            
            code = row[0].strip()
            name = row[1].strip()

            try:
                city = City.objects.get(code=code)
                if city.name != name:
                    city.name = name
                    city.save()
                    stats['updated'] += 1
                else:
                    stats['skipped'] += 1
            except City.DoesNotExist:
                City.objects.create(code=code, name=name)
                stats['created'] += 1
                
        self.stdout.write(
            f"Cities: {stats['created']} created, {stats['updated']} updated, {stats['skipped']} skipped."
        )

    def _process_hotels(self, rows):
        stats = {'created': 0, 'updated': 0, 'skipped': 0, 'warnings': 0}
        
        for row in rows:
            if len(row) < 3: continue

            city_code = row[0].strip()
            zone_id = row[1].strip()
            name = row[2].strip()

            try:
                city = City.objects.get(code=city_code)
                
                try:
                    hotel = Hotel.objects.get(city=city, zone=zone_id)
                    if hotel.name != name:
                        hotel.name = name
                        hotel.save()
                        stats['updated'] += 1
                    else:
                        stats['skipped'] += 1
                except Hotel.DoesNotExist:
                    Hotel.objects.create(city=city, zone=zone_id, name=name)
                    stats['created'] += 1
                    
            except City.DoesNotExist:
                stats['warnings'] += 1
                self.stderr.write(self.style.WARNING(f"Hotel '{name}' skipped: City '{city_code}' not found."))
        
        self.stdout.write(
            f"Hotels: {stats['created']} created, {stats['updated']} updated, "
            f"{stats['skipped']} skipped, {stats['warnings']} warnings (invalid city)."
        )
