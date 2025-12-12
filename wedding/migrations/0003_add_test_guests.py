# Add test guests - this migration will definitely run

from django.db import migrations


def create_test_guests(apps, schema_editor):
    Guest = apps.get_model('wedding', 'Guest')
    
    test_guests = [
        {'name': 'Sharma Family', 'email': 'sharma001@email.com', 'phone': '9876543001', 'party_name': 'The Sharma Family', 'max_guests': 5, 'rsvp_code': 'X3X0LT8N', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True, 'has_responded': False, 'guest_count_mendhi': 0, 'guest_count_vidhi': 0, 'guest_count_wedding': 0, 'guest_count_reception': 0, 'dietary_restrictions': '', 'notes': ''},
        {'name': 'Patel Family', 'email': 'patel002@email.com', 'phone': '9876543002', 'party_name': 'The Patel Family', 'max_guests': 6, 'rsvp_code': 'OXMBS0RJ', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True, 'has_responded': False, 'guest_count_mendhi': 0, 'guest_count_vidhi': 0, 'guest_count_wedding': 0, 'guest_count_reception': 0, 'dietary_restrictions': '', 'notes': ''},
        {'name': 'Mehta Family', 'email': 'mehta003@email.com', 'phone': '9876543003', 'party_name': 'The Mehta Family', 'max_guests': 4, 'rsvp_code': '1L1EFLX3', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True, 'has_responded': False, 'guest_count_mendhi': 0, 'guest_count_vidhi': 0, 'guest_count_wedding': 0, 'guest_count_reception': 0, 'dietary_restrictions': '', 'notes': ''},
        {'name': 'Test Guest', 'email': 'test@email.com', 'phone': '1234567890', 'party_name': 'Test Party', 'max_guests': 4, 'rsvp_code': 'TESTCODE', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True, 'has_responded': False, 'guest_count_mendhi': 0, 'guest_count_vidhi': 0, 'guest_count_wedding': 0, 'guest_count_reception': 0, 'dietary_restrictions': '', 'notes': ''},
    ]
    
    for guest_data in test_guests:
        Guest.objects.get_or_create(
            rsvp_code=guest_data['rsvp_code'],
            defaults=guest_data
        )
    
    print(f"Created/verified {len(test_guests)} guests")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0002_load_initial_guests'),
    ]

    operations = [
        migrations.RunPython(create_test_guests, reverse_func),
    ]

