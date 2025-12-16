from django.core.management.base import BaseCommand
from wedding.models import Guest, FamilyMember


class Command(BaseCommand):
    help = 'Create 5 families with individual member event invitations'

    def handle(self, *args, **options):
        # Clear existing data
        FamilyMember.objects.all().delete()
        Guest.objects.all().delete()
        self.stdout.write('Cleared existing families and members')
        
        # Define 5 families with their members and invitations
        families_data = [
            {
                'family': {
                    'name': 'Desai Family',
                    'party_name': 'The Desai Family',
                    'email': 'desai@email.com',
                    'phone': '9876543001',
                    'rsvp_code': 'DESAI001',
                },
                'members': [
                    {'name': 'Rajesh Desai', 'relation': 'father', 'invited_mendhi': False, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Priya Desai', 'relation': 'mother', 'invited_mendhi': False, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Arjun Desai', 'relation': 'son', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Vikram Desai', 'relation': 'son', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Ananya Desai', 'relation': 'daughter', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                ]
            },
            {
                'family': {
                    'name': 'Patel Family',
                    'party_name': 'The Patel Family',
                    'email': 'patel@email.com',
                    'phone': '9876543002',
                    'rsvp_code': 'PATEL001',
                },
                'members': [
                    {'name': 'Suresh Patel', 'relation': 'father', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Meena Patel', 'relation': 'mother', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Rohan Patel', 'relation': 'son', 'invited_mendhi': True, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Kavya Patel', 'relation': 'daughter', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                ]
            },
            {
                'family': {
                    'name': 'Sharma Family',
                    'party_name': 'The Sharma Family',
                    'email': 'sharma@email.com',
                    'phone': '9876543003',
                    'rsvp_code': 'SHARMA01',
                },
                'members': [
                    {'name': 'Anil Sharma', 'relation': 'father', 'invited_mendhi': False, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Sunita Sharma', 'relation': 'mother', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Amit Sharma', 'relation': 'son', 'invited_mendhi': False, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': False},
                    {'name': 'Neha Sharma', 'relation': 'daughter', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Pooja Sharma', 'relation': 'daughter', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Dadaji Sharma', 'relation': 'grandfather', 'invited_mendhi': False, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                ]
            },
            {
                'family': {
                    'name': 'Mehta Family',
                    'party_name': 'The Mehta Family',
                    'email': 'mehta@email.com',
                    'phone': '9876543004',
                    'rsvp_code': 'MEHTA001',
                },
                'members': [
                    {'name': 'Dinesh Mehta', 'relation': 'father', 'invited_mendhi': True, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Rekha Mehta', 'relation': 'mother', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Karan Mehta', 'relation': 'son', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                ]
            },
            {
                'family': {
                    'name': 'Singh Family',
                    'party_name': 'The Singh Family',
                    'email': 'singh@email.com',
                    'phone': '9876543005',
                    'rsvp_code': 'SINGH001',
                },
                'members': [
                    {'name': 'Harpreet Singh', 'relation': 'father', 'invited_mendhi': False, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Gurpreet Singh', 'relation': 'mother', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Jasmine Singh', 'relation': 'daughter', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Manpreet Singh', 'relation': 'son', 'invited_mendhi': True, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                    {'name': 'Dadi Singh', 'relation': 'grandmother', 'invited_mendhi': False, 'invited_vidhi': False, 'invited_wedding': True, 'invited_reception': True},
                ]
            },
        ]
        
        for family_data in families_data:
            # Create the family (Guest)
            family = Guest.objects.create(
                name=family_data['family']['name'],
                party_name=family_data['family']['party_name'],
                email=family_data['family']['email'],
                phone=family_data['family']['phone'],
                rsvp_code=family_data['family']['rsvp_code'],
                max_guests=len(family_data['members']),
            )
            
            self.stdout.write(f"\nCreated family: {family.party_name} (Code: {family.rsvp_code})")
            
            # Create members
            for i, member_data in enumerate(family_data['members']):
                member = FamilyMember.objects.create(
                    family=family,
                    name=member_data['name'],
                    relation=member_data['relation'],
                    invited_mendhi=member_data['invited_mendhi'],
                    invited_vidhi=member_data['invited_vidhi'],
                    invited_wedding=member_data['invited_wedding'],
                    invited_reception=member_data['invited_reception'],
                    order=i,
                )
                events = []
                if member.invited_mendhi: events.append('M')
                if member.invited_vidhi: events.append('V')
                if member.invited_wedding: events.append('W')
                if member.invited_reception: events.append('R')
                self.stdout.write(f"  - {member.name} ({member.get_relation_display()}): {', '.join(events)}")
        
        self.stdout.write(self.style.SUCCESS(f'\nSetup complete! Created {Guest.objects.count()} families with {FamilyMember.objects.count()} total members'))
