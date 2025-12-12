from django import forms
from .models import Guest


class RSVPCodeForm(forms.Form):
    """Form for entering RSVP code to access invitation"""
    rsvp_code = forms.CharField(
        max_length=8,
        min_length=8,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your 8-character code',
            'class': 'rsvp-code-input',
            'autocomplete': 'off',
            'autofocus': True,
            'style': 'text-transform: uppercase; letter-spacing: 3px; text-align: center; font-size: 1.5rem;',
        }),
        label='Your RSVP Code',
        help_text='Enter the unique code from your invitation'
    )
    
    def clean_rsvp_code(self):
        code = self.cleaned_data['rsvp_code'].upper().strip()
        try:
            guest = Guest.objects.get(rsvp_code=code)
            self.guest = guest
        except Guest.DoesNotExist:
            raise forms.ValidationError(
                'Invalid RSVP code. Please check your invitation and try again.'
            )
        return code


class GuestRSVPForm(forms.Form):
    """Dynamic form for guest RSVP based on their invited events"""
    
    RSVP_CHOICES = [
        ('attending', 'Yes, I will attend'),
        ('not_attending', 'Sorry, I cannot attend'),
    ]
    
    def __init__(self, guest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guest = guest
        
        # Dynamically add fields based on which events the guest is invited to
        if guest.invited_mendhi:
            self.fields['rsvp_mendhi'] = forms.ChoiceField(
                choices=self.RSVP_CHOICES,
                widget=forms.RadioSelect(attrs={'class': 'rsvp-radio'}),
                label='Mendhi - December 25, 2025',
                required=True,
                initial=guest.rsvp_mendhi if guest.rsvp_mendhi != 'pending' else None
            )
            self.fields['guests_mendhi'] = forms.IntegerField(
                min_value=0,
                max_value=guest.max_guests,
                initial=guest.guests_mendhi or 1,
                widget=forms.NumberInput(attrs={
                    'class': 'guest-count-input',
                    'min': 0,
                    'max': guest.max_guests,
                }),
                label=f'Number of guests attending (max {guest.max_guests})',
                required=False
            )
        
        if guest.invited_vidhi:
            self.fields['rsvp_vidhi'] = forms.ChoiceField(
                choices=self.RSVP_CHOICES,
                widget=forms.RadioSelect(attrs={'class': 'rsvp-radio'}),
                label='Vidhi - December 26, 2025',
                required=True,
                initial=guest.rsvp_vidhi if guest.rsvp_vidhi != 'pending' else None
            )
            self.fields['guests_vidhi'] = forms.IntegerField(
                min_value=0,
                max_value=guest.max_guests,
                initial=guest.guests_vidhi or 1,
                widget=forms.NumberInput(attrs={
                    'class': 'guest-count-input',
                    'min': 0,
                    'max': guest.max_guests,
                }),
                label=f'Number of guests attending (max {guest.max_guests})',
                required=False
            )
        
        if guest.invited_wedding:
            self.fields['rsvp_wedding'] = forms.ChoiceField(
                choices=self.RSVP_CHOICES,
                widget=forms.RadioSelect(attrs={'class': 'rsvp-radio'}),
                label='Wedding Ceremony - December 27, 2025',
                required=True,
                initial=guest.rsvp_wedding if guest.rsvp_wedding != 'pending' else None
            )
            self.fields['guests_wedding'] = forms.IntegerField(
                min_value=0,
                max_value=guest.max_guests,
                initial=guest.guests_wedding or 1,
                widget=forms.NumberInput(attrs={
                    'class': 'guest-count-input',
                    'min': 0,
                    'max': guest.max_guests,
                }),
                label=f'Number of guests attending (max {guest.max_guests})',
                required=False
            )
        
        if guest.invited_reception:
            self.fields['rsvp_reception'] = forms.ChoiceField(
                choices=self.RSVP_CHOICES,
                widget=forms.RadioSelect(attrs={'class': 'rsvp-radio'}),
                label='Reception - December 28, 2025',
                required=True,
                initial=guest.rsvp_reception if guest.rsvp_reception != 'pending' else None
            )
            self.fields['guests_reception'] = forms.IntegerField(
                min_value=0,
                max_value=guest.max_guests,
                initial=guest.guests_reception or 1,
                widget=forms.NumberInput(attrs={
                    'class': 'guest-count-input',
                    'min': 0,
                    'max': guest.max_guests,
                }),
                label=f'Number of guests attending (max {guest.max_guests})',
                required=False
            )
        
        # Additional fields
        self.fields['dietary_requirements'] = forms.CharField(
            widget=forms.Textarea(attrs={
                'placeholder': 'Please let us know of any dietary requirements or allergies',
                'rows': 3,
                'class': 'form-textarea',
            }),
            label='Dietary Requirements',
            required=False,
            initial=guest.dietary_requirements
        )
        
        self.fields['message'] = forms.CharField(
            widget=forms.Textarea(attrs={
                'placeholder': 'Share your wishes or a message for us',
                'rows': 3,
                'class': 'form-textarea',
            }),
            label='Message for the Couple',
            required=False,
            initial=guest.message
        )
    
    def save(self):
        """Save the RSVP response to the guest record"""
        guest = self.guest
        
        # Update RSVP status for each invited event
        if guest.invited_mendhi and 'rsvp_mendhi' in self.cleaned_data:
            guest.rsvp_mendhi = self.cleaned_data['rsvp_mendhi']
            if self.cleaned_data['rsvp_mendhi'] == 'attending':
                guest.guests_mendhi = self.cleaned_data.get('guests_mendhi', 1) or 1
            else:
                guest.guests_mendhi = 0
        
        if guest.invited_vidhi and 'rsvp_vidhi' in self.cleaned_data:
            guest.rsvp_vidhi = self.cleaned_data['rsvp_vidhi']
            if self.cleaned_data['rsvp_vidhi'] == 'attending':
                guest.guests_vidhi = self.cleaned_data.get('guests_vidhi', 1) or 1
            else:
                guest.guests_vidhi = 0
        
        if guest.invited_wedding and 'rsvp_wedding' in self.cleaned_data:
            guest.rsvp_wedding = self.cleaned_data['rsvp_wedding']
            if self.cleaned_data['rsvp_wedding'] == 'attending':
                guest.guests_wedding = self.cleaned_data.get('guests_wedding', 1) or 1
            else:
                guest.guests_wedding = 0
        
        if guest.invited_reception and 'rsvp_reception' in self.cleaned_data:
            guest.rsvp_reception = self.cleaned_data['rsvp_reception']
            if self.cleaned_data['rsvp_reception'] == 'attending':
                guest.guests_reception = self.cleaned_data.get('guests_reception', 1) or 1
            else:
                guest.guests_reception = 0
        
        # Update additional info
        guest.dietary_requirements = self.cleaned_data.get('dietary_requirements', '')
        guest.message = self.cleaned_data.get('message', '')
        
        # Mark as responded
        guest.mark_as_responded()
        
        return guest


class GuestImportForm(forms.Form):
    """Form for importing guests from CSV"""
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with guest information'
    )


class ForgotCodeForm(forms.Form):
    """Form for guests who forgot their RSVP code"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'forgot-code-input',
            'autocomplete': 'email',
            'autofocus': True,
        }),
        label='Email Address',
        help_text='Enter the email address from your invitation'
    )
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        from .models import Guest
        try:
            guest = Guest.objects.get(email__iexact=email)
            self.guest = guest
        except Guest.DoesNotExist:
            raise forms.ValidationError(
                'We could not find an invitation with this email address. '
                'Please check the email or contact the couple directly.'
            )
        except Guest.MultipleObjectsReturned:
            # If multiple guests have same email, get the first one
            self.guest = Guest.objects.filter(email__iexact=email).first()
        return email
