from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hotels.models import City

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users for development (superuser and Amsterdam manager)'

    def handle(self, *args, **options):
        self.stdout.write('Creating test users...')
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='maykinmedia',
                email='admin@maykinmedia.nl'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superuser "admin" created'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Superuser "admin" already exists'))
        
        # Create Amsterdam manager
        if not User.objects.filter(username='hotels_amsterdam').exists():
            # Get Amsterdam city
            try:
                amsterdam = City.objects.get(code='AMS')
            except City.DoesNotExist:
                self.stdout.write(self.style.ERROR('✗ Amsterdam city not found! Make sure to run import_hotel_data first.'))
                return
            
            # Create the user
            user = User.objects.create_user(
                username='hotels_amsterdam',
                password='maykinmedia',
                email='amsterdam@maykinmedia.nl',
                city=amsterdam,
                is_staff=True  # Give staff permissions to access admin
            )
            
            # Grant all hotel permissions
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType
            from hotels.models import Hotel
            
            hotel_content_type = ContentType.objects.get_for_model(Hotel)
            permissions = Permission.objects.filter(content_type=hotel_content_type)
            user.user_permissions.set(permissions)
            
            self.stdout.write(self.style.SUCCESS('✓ Amsterdam manager "hotels_amsterdam" created'))
        else:
            self.stdout.write(self.style.WARNING('⚠ User "hotels_amsterdam" already exists'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Test Users ==='))
        self.stdout.write('Superuser:')
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: maykinmedia')
        self.stdout.write('')
        self.stdout.write('Amsterdam Manager:')
        self.stdout.write('  Username: hotels_amsterdam')
        self.stdout.write('  Password: maykinmedia')
        self.stdout.write('  City: Amsterdam (AMS)')
