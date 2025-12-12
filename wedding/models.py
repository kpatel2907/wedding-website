import uuid
import secrets
import string
from django.db import models
from django.utils import timezone


def generate_rsvp_code():
    """Generate a unique 8-character RSVP code"""
    # Use uppercase letters and digits, excluding confusing characters (0, O, I, L, 1)
    alphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    return ''.join(secrets.choice(alphabet) for _ in range(8))


class Event(models.Model):
    """Wedding event model (Mendhi, Vidhi, Wedding, Reception)"""
    EVENT_CHOICES = [
        ('mendhi', 'Mendhi'),
        ('vidhi', 'Vidhi'),
        ('wedding', 'Wedding'),
        ('reception', 'Reception'),
    ]
    
    slug = models.CharField(max_length=20, choices=EVENT_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, help_text="Emoji or symbol for the event")
    date = models.DateField()
    time = models.CharField(max_length=50)
    venue_name = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=300)
    description = models.TextField()
    dress_code = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'date']

    def __str__(self):
        return f"{self.name} - {self.date}"


class StoryMilestone(models.Model):
    """Timeline milestone for the couple's story"""
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.year} - {self.title}"


class Guest(models.Model):
    """
    Guest model with unique RSVP code.
    Each guest has their own private code and can only RSVP to events they're invited to.
    """
    RSVP_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('attending', 'Attending'),
        ('not_attending', 'Not Attending'),
    ]
    
    # Guest identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rsvp_code = models.CharField(
        max_length=8, 
        unique=True, 
        default=generate_rsvp_code,
        help_text="Unique 8-character code for private RSVP access"
    )
    
    # Guest information
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Party/Group information
    party_name = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Family or group name (e.g., 'The Smith Family')"
    )
    max_guests = models.PositiveIntegerField(
        default=1,
        help_text="Maximum number of guests in this party (including primary guest)"
    )
    
    # Event invitations (which events this guest is invited to)
    invited_mendhi = models.BooleanField(default=False)
    invited_vidhi = models.BooleanField(default=False)
    invited_wedding = models.BooleanField(default=False)
    invited_reception = models.BooleanField(default=False)
    
    # RSVP responses
    rsvp_mendhi = models.CharField(max_length=20, choices=RSVP_STATUS_CHOICES, default='pending')
    rsvp_vidhi = models.CharField(max_length=20, choices=RSVP_STATUS_CHOICES, default='pending')
    rsvp_wedding = models.CharField(max_length=20, choices=RSVP_STATUS_CHOICES, default='pending')
    rsvp_reception = models.CharField(max_length=20, choices=RSVP_STATUS_CHOICES, default='pending')
    
    # Guest counts for each event
    guests_mendhi = models.PositiveIntegerField(default=0)
    guests_vidhi = models.PositiveIntegerField(default=0)
    guests_wedding = models.PositiveIntegerField(default=0)
    guests_reception = models.PositiveIntegerField(default=0)
    
    # Additional information
    dietary_requirements = models.TextField(blank=True)
    message = models.TextField(blank=True, help_text="Message from the guest")
    notes = models.TextField(blank=True, help_text="Admin notes about this guest")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rsvp_submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    has_responded = models.BooleanField(default=False)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Guest"
        verbose_name_plural = "Guests"

    def __str__(self):
        return f"{self.name} ({self.rsvp_code})"
    
    def save(self, *args, **kwargs):
        # Ensure RSVP code is unique
        if not self.rsvp_code:
            self.rsvp_code = generate_rsvp_code()
            while Guest.objects.filter(rsvp_code=self.rsvp_code).exists():
                self.rsvp_code = generate_rsvp_code()
        super().save(*args, **kwargs)
    
    @property
    def invited_events(self):
        """Return list of events this guest is invited to"""
        events = []
        if self.invited_mendhi:
            events.append('mendhi')
        if self.invited_vidhi:
            events.append('vidhi')
        if self.invited_wedding:
            events.append('wedding')
        if self.invited_reception:
            events.append('reception')
        return events
    
    @property
    def invited_events_display(self):
        """Return human-readable list of invited events"""
        events = []
        if self.invited_mendhi:
            events.append('Mendhi')
        if self.invited_vidhi:
            events.append('Vidhi')
        if self.invited_wedding:
            events.append('Wedding')
        if self.invited_reception:
            events.append('Reception')
        return ', '.join(events) if events else 'None'
    
    @property
    def rsvp_summary(self):
        """Return summary of RSVP responses"""
        responses = []
        if self.invited_mendhi:
            responses.append(f"Mendhi: {self.get_rsvp_mendhi_display()}")
        if self.invited_vidhi:
            responses.append(f"Vidhi: {self.get_rsvp_vidhi_display()}")
        if self.invited_wedding:
            responses.append(f"Wedding: {self.get_rsvp_wedding_display()}")
        if self.invited_reception:
            responses.append(f"Reception: {self.get_rsvp_reception_display()}")
        return ' | '.join(responses)
    
    @property
    def total_attending_count(self):
        """Total number of guests attending across all events"""
        total = 0
        if self.rsvp_mendhi == 'attending':
            total += self.guests_mendhi
        if self.rsvp_vidhi == 'attending':
            total += self.guests_vidhi
        if self.rsvp_wedding == 'attending':
            total += self.guests_wedding
        if self.rsvp_reception == 'attending':
            total += self.guests_reception
        return total
    
    def mark_as_responded(self):
        """Mark this guest as having responded"""
        self.has_responded = True
        self.rsvp_submitted_at = timezone.now()
        self.save(update_fields=['has_responded', 'rsvp_submitted_at', 'updated_at'])


class WeddingInfo(models.Model):
    """General wedding information (singleton model)"""
    partner1_name = models.CharField(max_length=100, default="Sarah")
    partner2_name = models.CharField(max_length=100, default="Michael")
    wedding_date = models.DateField()
    location = models.CharField(max_length=200, default="Mumbai, India")
    hashtag = models.CharField(max_length=100, default="#SarahAndMichaelForever")
    welcome_title = models.CharField(max_length=200, default="Welcome to Our Wedding")
    welcome_message = models.TextField()

    class Meta:
        verbose_name = "Wedding Info"
        verbose_name_plural = "Wedding Info"

    def __str__(self):
        return f"{self.partner1_name} & {self.partner2_name}'s Wedding"


# Keep the old RSVP model for backward compatibility (can be removed later)
class RSVP(models.Model):
    """Legacy RSVP model - kept for migration compatibility"""
    GUEST_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    guests = models.PositiveIntegerField(choices=GUEST_CHOICES, default=1)
    attending_mendhi = models.BooleanField(default=False)
    attending_vidhi = models.BooleanField(default=False)
    attending_wedding = models.BooleanField(default=False)
    attending_reception = models.BooleanField(default=False)
    dietary_requirements = models.TextField(blank=True)
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "RSVP (Legacy)"
        verbose_name_plural = "RSVPs (Legacy)"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.email}"
