from django.core.management.base import BaseCommand
from wedding.models import Guest


class Command(BaseCommand):
    help = 'Create initial test guests and update existing guests to max 10'

    def handle(self, *args, **options):
        # First, update all existing guests to have max_guests = 10
        updated = Guest.objects.all().update(max_guests=10)
        if updated:
            self.stdout.write(self.style.SUCCESS(f'Updated {updated} guests to max_guests=10'))
        
        # Create test guests if none exist
        if Guest.objects.count() < 5:
            guests_data = [
                {'name': 'Sharma Family', 'email': 'sharma001@email.com', 'phone': '9876543001', 'party_name': 'The Sharma Family', 'max_guests': 10, 'rsvp_code': 'SHARMA01', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                {'name': 'Patel Family', 'email': 'patel002@email.com', 'phone': '9876543002', 'party_name': 'The Patel Family', 'max_guests': 10, 'rsvp_code': 'PATEL002', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                {'name': 'Mehta Family', 'email': 'mehta003@email.com', 'phone': '9876543003', 'party_name': 'The Mehta Family', 'max_guests': 10, 'rsvp_code': 'MEHTA003', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                {'name': 'Desai Family', 'email': 'desai004@email.com', 'phone': '9876543004', 'party_name': 'The Desai Family', 'max_guests': 10, 'rsvp_code': 'DESAI004', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                {'name': 'Test Guest', 'email': 'test@email.com', 'phone': '1234567890', 'party_name': 'Test Party', 'max_guests': 10, 'rsvp_code': 'TESTCODE', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            ]
            
            for data in guests_data:
                guest, created = Guest.objects.get_or_create(
                    rsvp_code=data['rsvp_code'],
                    defaults=data
                )
                if created:
                    self.stdout.write(f"Created guest: {data['name']} with code {data['rsvp_code']}")
            
            self.stdout.write(self.style.SUCCESS('Guest setup complete!'))
        else:
            self.stdout.write(self.style.SUCCESS('Guests already exist'))
