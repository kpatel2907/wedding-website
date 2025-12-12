from django.core.management.base import BaseCommand
from wedding.models import Guest


class Command(BaseCommand):
    help = 'Create initial test guests and update existing guests to max 10'

    def handle(self, *args, **options):
        # First, update all existing guests to have max_guests = 10
        updated = Guest.objects.all().update(max_guests=10)
        if updated:
            self.stdout.write(self.style.SUCCESS(f'Updated {updated} guests to max_guests=10'))
        
        # All guests to create/ensure exist
        guests_data = [
            # Original 5
            {'name': 'Sharma Family', 'email': 'sharma001@email.com', 'phone': '9876543001', 'party_name': 'The Sharma Family', 'max_guests': 10, 'rsvp_code': 'SHARMA01', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Patel Family', 'email': 'patel002@email.com', 'phone': '9876543002', 'party_name': 'The Patel Family', 'max_guests': 10, 'rsvp_code': 'PATEL002', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Mehta Family', 'email': 'mehta003@email.com', 'phone': '9876543003', 'party_name': 'The Mehta Family', 'max_guests': 10, 'rsvp_code': 'MEHTA003', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Desai Family', 'email': 'desai004@email.com', 'phone': '9876543004', 'party_name': 'The Desai Family', 'max_guests': 10, 'rsvp_code': 'DESAI004', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Test Guest', 'email': 'test@email.com', 'phone': '1234567890', 'party_name': 'Test Party', 'max_guests': 10, 'rsvp_code': 'TESTCODE', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            # New 10 guests
            {'name': 'Singh Family', 'email': 'singh005@email.com', 'phone': '9876543005', 'party_name': 'The Singh Family', 'max_guests': 10, 'rsvp_code': 'SINGH005', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Gupta Family', 'email': 'gupta006@email.com', 'phone': '9876543006', 'party_name': 'The Gupta Family', 'max_guests': 10, 'rsvp_code': 'GUPTA006', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Kumar Family', 'email': 'kumar007@email.com', 'phone': '9876543007', 'party_name': 'The Kumar Family', 'max_guests': 10, 'rsvp_code': 'KUMAR007', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Joshi Family', 'email': 'joshi008@email.com', 'phone': '9876543008', 'party_name': 'The Joshi Family', 'max_guests': 10, 'rsvp_code': 'JOSHI008', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Verma Family', 'email': 'verma009@email.com', 'phone': '9876543009', 'party_name': 'The Verma Family', 'max_guests': 10, 'rsvp_code': 'VERMA009', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Reddy Family', 'email': 'reddy010@email.com', 'phone': '9876543010', 'party_name': 'The Reddy Family', 'max_guests': 10, 'rsvp_code': 'REDDY010', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Agarwal Family', 'email': 'agarwal011@email.com', 'phone': '9876543011', 'party_name': 'The Agarwal Family', 'max_guests': 10, 'rsvp_code': 'AGARWAL1', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Malhotra Family', 'email': 'malhotra012@email.com', 'phone': '9876543012', 'party_name': 'The Malhotra Family', 'max_guests': 10, 'rsvp_code': 'MALHOTR1', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Kapoor Family', 'email': 'kapoor013@email.com', 'phone': '9876543013', 'party_name': 'The Kapoor Family', 'max_guests': 10, 'rsvp_code': 'KAPOOR01', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
            {'name': 'Iyer Family', 'email': 'iyer014@email.com', 'phone': '9876543014', 'party_name': 'The Iyer Family', 'max_guests': 10, 'rsvp_code': 'IYER0014', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        ]
        
        created_count = 0
        for data in guests_data:
            guest, created = Guest.objects.get_or_create(
                rsvp_code=data['rsvp_code'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created guest: {data['name']} with code {data['rsvp_code']}")
        
        self.stdout.write(self.style.SUCCESS(f'Guest setup complete! Created {created_count} new guests. Total: {Guest.objects.count()}'))
