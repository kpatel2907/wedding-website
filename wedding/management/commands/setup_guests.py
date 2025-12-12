from django.core.management.base import BaseCommand
from wedding.models import Guest


class Command(BaseCommand):
    help = 'Create initial test guests'

    def handle(self, *args, **options):
        # Check if guests already exist
        if Guest.objects.exists():
            self.stdout.write(self.style.WARNING('Guests already exist, skipping'))
            return
        
        guests_data = [
            {'name': 'Sharma Family', 'email': 'sharma001@email.com', 'phone': '9876543001', 'party_name': 'The Sharma Family', 'max_guests': 5, 'rsvp_code': 'SHARMA01', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Patel Family', 'email': 'patel002@email.com', 'phone': '9876543002', 'party_name': 'The Patel Family', 'max_guests': 6, 'rsvp_code': 'PATEL002', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Mehta Family', 'email': 'mehta003@email.com', 'phone': '9876543003', 'party_name': 'The Mehta Family', 'max_guests': 4, 'rsvp_code': 'MEHTA003', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Desai Family', 'email': 'desai004@email.com', 'phone': '9876543004', 'party_name': 'The Desai Family', 'max_guests': 5, 'rsvp_code': 'DESAI004', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Test Guest', 'email': 'test@email.com', 'phone': '1234567890', 'party_name': 'Test Party', 'max_guests': 4, 'rsvp_code': 'TESTCODE', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        ]
        
        for data in guests_data:
            Guest.objects.create(**data)
            self.stdout.write(f"Created guest: {data['name']} with code {data['rsvp_code']}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(guests_data)} guests'))

