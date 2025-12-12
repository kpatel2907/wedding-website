# Add guests with correct field names

from django.db import migrations


def create_guests(apps, schema_editor):
    Guest = apps.get_model('wedding', 'Guest')
    
    # Skip if guests already exist
    if Guest.objects.exists():
        print("Guests already exist, skipping")
        return
    
    guests_data = [
        {'name': 'Sharma Family', 'email': 'sharma001@email.com', 'phone': '9876543001', 'party_name': 'The Sharma Family', 'max_guests': 5, 'rsvp_code': 'SHARMA01', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        {'name': 'Patel Family', 'email': 'patel002@email.com', 'phone': '9876543002', 'party_name': 'The Patel Family', 'max_guests': 6, 'rsvp_code': 'PATEL002', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        {'name': 'Mehta Family', 'email': 'mehta003@email.com', 'phone': '9876543003', 'party_name': 'The Mehta Family', 'max_guests': 4, 'rsvp_code': 'MEHTA003', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        {'name': 'Desai Family', 'email': 'desai004@email.com', 'phone': '9876543004', 'party_name': 'The Desai Family', 'max_guests': 5, 'rsvp_code': 'DESAI004', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        {'name': 'Singh Family', 'email': 'singh005@email.com', 'phone': '9876543005', 'party_name': 'The Singh Family', 'max_guests': 4, 'rsvp_code': 'SINGH005', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
        {'name': 'Test Guest', 'email': 'test@email.com', 'phone': '1234567890', 'party_name': 'Test Party', 'max_guests': 4, 'rsvp_code': 'TESTCODE', 'invited_mendhi': True, 'invited_vidhi': True, 'invited_wedding': True, 'invited_reception': True},
    ]
    
    for data in guests_data:
        Guest.objects.create(**data)
    
    print(f"Created {len(guests_data)} guests successfully!")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0003_add_test_guests'),
    ]

    operations = [
        migrations.RunPython(create_guests, reverse_func),
    ]

