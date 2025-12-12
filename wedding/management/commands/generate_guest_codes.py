"""
Management command to generate/export guest list with RSVP codes.

Usage:
    python manage.py generate_guest_codes --output guests_with_codes.csv
"""

import csv
from django.core.management.base import BaseCommand
from wedding.models import Guest


class Command(BaseCommand):
    help = 'Export guest list with RSVP codes to CSV'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='guests_with_codes.csv',
            help='Output CSV file path',
        )
    
    def handle(self, *args, **options):
        output_file = options['output']
        
        guests = Guest.objects.all().order_by('name')
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Name', 'RSVP Code', 'Email', 'Phone', 'Party Name', 'Max Guests',
                'Invited Mendhi', 'Invited Vidhi', 'Invited Wedding', 'Invited Reception',
                'RSVP Link'
            ])
            
            for guest in guests:
                rsvp_link = f"https://yourwebsite.com/rsvp/{guest.rsvp_code}/"
                writer.writerow([
                    guest.name,
                    guest.rsvp_code,
                    guest.email,
                    guest.phone,
                    guest.party_name,
                    guest.max_guests,
                    'Yes' if guest.invited_mendhi else 'No',
                    'Yes' if guest.invited_vidhi else 'No',
                    'Yes' if guest.invited_wedding else 'No',
                    'Yes' if guest.invited_reception else 'No',
                    rsvp_link,
                ])
        
        self.stdout.write(self.style.SUCCESS(
            f'Exported {guests.count()} guests to {output_file}'
        ))

