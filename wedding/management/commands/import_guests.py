"""
Management command to import guests from a CSV file.

Usage:
    python manage.py import_guests path/to/guests.csv

CSV Format:
    name,email,phone,party_name,max_guests,invited_mendhi,invited_vidhi,invited_wedding,invited_reception
    
Example:
    "John Smith","john@email.com","555-1234","The Smith Family",4,True,True,True,True
    "Jane Doe","jane@email.com","555-5678","",2,False,False,True,True
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from wedding.models import Guest


class Command(BaseCommand):
    help = 'Import guests from a CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing guests if they match by name/email',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )
    
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        update_existing = options['update']
        dry_run = options['dry_run']
        
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                created_count = 0
                updated_count = 0
                skipped_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 for header)
                    try:
                        # Parse row data
                        name = row.get('name', '').strip()
                        email = row.get('email', '').strip()
                        phone = row.get('phone', '').strip()
                        party_name = row.get('party_name', '').strip()
                        
                        # Parse max_guests (default to 1)
                        try:
                            max_guests = int(row.get('max_guests', 1) or 1)
                        except ValueError:
                            max_guests = 1
                        
                        # Parse boolean fields
                        invited_mendhi = self._parse_bool(row.get('invited_mendhi', 'False'))
                        invited_vidhi = self._parse_bool(row.get('invited_vidhi', 'False'))
                        invited_wedding = self._parse_bool(row.get('invited_wedding', 'False'))
                        invited_reception = self._parse_bool(row.get('invited_reception', 'False'))
                        
                        if not name:
                            errors.append(f"Row {row_num}: Name is required")
                            continue
                        
                        if dry_run:
                            self.stdout.write(
                                f"Would import: {name} (Email: {email}, Party: {max_guests}, "
                                f"Events: M={invited_mendhi}, V={invited_vidhi}, W={invited_wedding}, R={invited_reception})"
                            )
                            created_count += 1
                            continue
                        
                        # Check if guest exists
                        existing_guest = None
                        if email:
                            existing_guest = Guest.objects.filter(email__iexact=email).first()
                        if not existing_guest:
                            existing_guest = Guest.objects.filter(name__iexact=name).first()
                        
                        if existing_guest:
                            if update_existing:
                                existing_guest.email = email
                                existing_guest.phone = phone
                                existing_guest.party_name = party_name
                                existing_guest.max_guests = max_guests
                                existing_guest.invited_mendhi = invited_mendhi
                                existing_guest.invited_vidhi = invited_vidhi
                                existing_guest.invited_wedding = invited_wedding
                                existing_guest.invited_reception = invited_reception
                                existing_guest.save()
                                updated_count += 1
                                self.stdout.write(self.style.WARNING(f"Updated: {name}"))
                            else:
                                skipped_count += 1
                                self.stdout.write(f"Skipped (exists): {name}")
                        else:
                            Guest.objects.create(
                                name=name,
                                email=email,
                                phone=phone,
                                party_name=party_name,
                                max_guests=max_guests,
                                invited_mendhi=invited_mendhi,
                                invited_vidhi=invited_vidhi,
                                invited_wedding=invited_wedding,
                                invited_reception=invited_reception,
                            )
                            created_count += 1
                            self.stdout.write(self.style.SUCCESS(f"Created: {name}"))
                    
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                
                # Summary
                self.stdout.write("\n" + "=" * 50)
                if dry_run:
                    self.stdout.write(self.style.WARNING("DRY RUN - No changes made"))
                self.stdout.write(f"Created: {created_count}")
                self.stdout.write(f"Updated: {updated_count}")
                self.stdout.write(f"Skipped: {skipped_count}")
                
                if errors:
                    self.stdout.write(self.style.ERROR(f"\nErrors ({len(errors)}):"))
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"  - {error}"))
        
        except FileNotFoundError:
            raise CommandError(f'File not found: {csv_file}')
        except Exception as e:
            raise CommandError(f'Error reading CSV: {str(e)}')
    
    def _parse_bool(self, value):
        """Parse boolean value from CSV"""
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('true', 'yes', '1', 'y', 't')

