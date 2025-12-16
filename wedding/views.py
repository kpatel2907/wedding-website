from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q, Sum
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Event, StoryMilestone, WeddingInfo, Guest, FamilyMember
from .forms import RSVPCodeForm, GuestRSVPForm, ForgotCodeForm
import csv
import json


def home(request):
    """Main wedding website view with all sections"""
    # Get wedding info or use defaults
    wedding_info = WeddingInfo.objects.first()
    
    # Get events and story milestones
    events = Event.objects.all()
    milestones = StoryMilestone.objects.all()
    
    # Default wedding info if none exists
    if not wedding_info:
        wedding_info = {
            'partner1_name': 'Prit',
            'partner2_name': 'Khushboo',
            'wedding_date': '2025-12-28',
            'location': 'Mumbai, India',
            'hashtag': '#PritniKhushi',
            'welcome_title': 'Welcome to Our Wedding',
            'welcome_message': 'We are so excited to celebrate our special day with you! Join us for a beautiful celebration of love, laughter, and happily ever after.',
        }
    
    # Default milestones if none exist
    if not milestones:
        milestones = [
            {'year': '2018', 'title': 'How We Met', 'description': 'It all started at a mutual friend\'s birthday party. Across a crowded room, our eyes met, and we knew something magical was beginning.'},
            {'year': '2019', 'title': 'The First Date', 'description': 'Our first official date was at a cozy café downtown. We were both so nervous, but within minutes, it felt like we had known each other forever.'},
            {'year': '2021', 'title': 'Moving In Together', 'description': 'After two wonderful years of dating, we decided to take the next step. We found our perfect little apartment and started building our life together.'},
            {'year': '2024', 'title': 'The Proposal', 'description': 'On a beautiful sunset evening at our favorite beach, Michael got down on one knee and asked the question that would change our lives forever.'},
            {'year': '2025', 'title': 'Forever Begins', 'description': 'And now, we\'re ready to begin our forever journey together. We can\'t wait to celebrate this new chapter with all of you.'},
        ]
    
    # Default events if none exist
    if not events:
        events = [
            {'name': 'Mendhi', 'icon': '✿', 'date': 'December 25, 2025', 'time': '4:00 PM onwards', 'venue_name': 'The Garden Pavilion', 'venue_address': '123 Celebration Lane, Mumbai', 'description': 'Join us for an evening of beautiful henna designs, music, and dance.', 'dress_code': 'Colorful Indian Attire', 'is_featured': False},
            {'name': 'Vidhi', 'icon': '🪔', 'date': 'December 26, 2025', 'time': '10:00 AM - 2:00 PM', 'venue_name': 'Family Residence', 'venue_address': '456 Heritage Road, Mumbai', 'description': 'A sacred ceremony filled with traditional rituals and blessings.', 'dress_code': 'Traditional Indian Wear', 'is_featured': False},
            {'name': 'Wedding', 'icon': '💒', 'date': 'December 27, 2025', 'time': '6:00 PM onwards', 'venue_name': 'The Grand Ballroom', 'venue_address': '789 Royal Palace Hotel, Mumbai', 'description': 'The main event! Watch us exchange vows and become partners for life.', 'dress_code': 'Formal Indian / Western', 'is_featured': True},
            {'name': 'Reception', 'icon': '🎉', 'date': 'December 28, 2025', 'time': '7:00 PM onwards', 'venue_name': 'Starlight Terrace', 'venue_address': '789 Royal Palace Hotel, Mumbai', 'description': 'Let\'s dance the night away!', 'dress_code': 'Glamorous Evening Wear', 'is_featured': False},
        ]
    
    context = {
        'wedding_info': wedding_info,
        'events': events,
        'milestones': milestones,
    }
    
    return render(request, 'wedding/home.html', context)


def rsvp_lookup(request):
    """RSVP code lookup page - guests enter their unique code"""
    if request.method == 'POST':
        form = RSVPCodeForm(request.POST)
        if form.is_valid():
            guest = form.guest
            # Update last viewed timestamp
            guest.last_viewed_at = timezone.now()
            guest.save(update_fields=['last_viewed_at'])
            # Redirect to the RSVP form with the code
            return redirect('wedding:rsvp_form', rsvp_code=guest.rsvp_code)
    else:
        form = RSVPCodeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'wedding/rsvp_lookup.html', context)


def forgot_code(request):
    """Handle forgot RSVP code - send code to guest's email"""
    email_sent = False
    
    if request.method == 'POST':
        form = ForgotCodeForm(request.POST)
        if form.is_valid():
            guest = form.guest
            
            # Get wedding info for email
            wedding_info = WeddingInfo.objects.first()
            couple_names = "Prit & Khushboo"
            if wedding_info:
                couple_names = f"{wedding_info.partner1_name} & {wedding_info.partner2_name}"
            
            # Build the RSVP link
            rsvp_link = request.build_absolute_uri(f'/rsvp/{guest.rsvp_code}/')
            
            # Send email
            subject = f"Your RSVP Code for {couple_names}'s Wedding"
            
            message = f"""
Dear {guest.name},

You requested your RSVP code for {couple_names}'s wedding celebration.

Your RSVP Code: {guest.rsvp_code}

You can use this code to RSVP at: {rsvp_link}

Or simply click the link above to go directly to your invitation.

We look forward to celebrating with you!

With love,
{couple_names}
            """
            
            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Georgia', serif; background-color: #faf8f5; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #b8860b; font-size: 28px; margin: 0; }}
        .content {{ color: #333; line-height: 1.8; }}
        .code-box {{ background: #f5e6d3; padding: 20px; text-align: center; border-radius: 10px; margin: 25px 0; }}
        .code {{ font-size: 32px; font-weight: bold; color: #b8860b; letter-spacing: 5px; }}
        .btn {{ display: inline-block; background: #b8860b; color: white; padding: 15px 40px; text-decoration: none; border-radius: 8px; margin-top: 20px; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💌 Your RSVP Code</h1>
        </div>
        <div class="content">
            <p>Dear <strong>{guest.name}</strong>,</p>
            <p>You requested your RSVP code for <strong>{couple_names}'s</strong> wedding celebration.</p>
            
            <div class="code-box">
                <p style="margin: 0 0 10px 0; color: #666;">Your RSVP Code:</p>
                <div class="code">{guest.rsvp_code}</div>
            </div>
            
            <p style="text-align: center;">
                <a href="{rsvp_link}" class="btn">RSVP Now</a>
            </p>
            
            <p>Or copy and paste this link in your browser:<br>
            <a href="{rsvp_link}">{rsvp_link}</a></p>
        </div>
        <div class="footer">
            <p>With love,<br><strong>{couple_names}</strong></p>
        </div>
    </div>
</body>
</html>
            """
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[guest.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                # If email fails, still show the success page but log the error
                print(f"Email sending failed: {e}")
                # For development, we'll still show success and display the code
                email_sent = True
            
            # Store guest info for success message
            request.session['forgot_code_guest'] = {
                'name': guest.name,
                'email': guest.email,
                'code': guest.rsvp_code,  # For development/testing
            }
            
            return redirect('wedding:forgot_code_sent')
    else:
        form = ForgotCodeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'wedding/forgot_code.html', context)


def forgot_code_sent(request):
    """Success page after sending forgot code email"""
    guest_info = request.session.get('forgot_code_guest', {})
    
    context = {
        'guest_name': guest_info.get('name', 'Guest'),
        'guest_email': guest_info.get('email', ''),
        'guest_code': guest_info.get('code', ''),  # For dev/testing display
    }
    return render(request, 'wedding/forgot_code_sent.html', context)


def rsvp_form(request, rsvp_code):
    """Private RSVP form for a family with individual members"""
    # Get the family by RSVP code
    family = get_object_or_404(Guest, rsvp_code=rsvp_code.upper())
    
    # Get family members
    members = family.members.all().order_by('order', 'name')
    
    # Get events for display
    events = Event.objects.all()
    
    # Build event details dict
    event_details = {}
    for event in events:
        event_details[event.slug] = {
            'name': event.name,
            'icon': event.icon,
            'date': event.date,
            'time': event.time,
            'venue_name': event.venue_name,
            'venue_address': event.venue_address,
            'description': event.description,
            'dress_code': event.dress_code,
        }
    
    # Default event details if no events in database
    if not event_details:
        event_details = {
            'mendhi': {'name': 'Mendhi', 'icon': '✿', 'date': 'December 25, 2025', 'time': '4:00 PM onwards', 'venue_name': 'The Garden Pavilion', 'venue_address': '123 Celebration Lane, Mumbai', 'dress_code': 'Colorful Indian Attire'},
            'vidhi': {'name': 'Vidhi', 'icon': '🪔', 'date': 'December 26, 2025', 'time': '10:00 AM - 2:00 PM', 'venue_name': 'Family Residence', 'venue_address': '456 Heritage Road, Mumbai', 'dress_code': 'Traditional Indian Wear'},
            'wedding': {'name': 'Wedding', 'icon': '💒', 'date': 'December 27, 2025', 'time': '6:00 PM onwards', 'venue_name': 'The Grand Ballroom', 'venue_address': '789 Royal Palace Hotel, Mumbai', 'dress_code': 'Formal Indian Attire'},
            'reception': {'name': 'Reception', 'icon': '🎉', 'date': 'December 28, 2025', 'time': '7:00 PM onwards', 'venue_name': 'Starlight Terrace', 'venue_address': '789 Royal Palace Hotel, Mumbai', 'dress_code': 'Semi-formal'},
        }
    
    rsvp_success = False
    
    if request.method == 'POST':
        # Process RSVP for each family member
        try:
            for member in members:
                member_id = str(member.id)
                
                # Update RSVP for each event the member is invited to
                if member.invited_mendhi:
                    rsvp_value = request.POST.get(f'rsvp_mendhi_{member_id}', 'pending')
                    member.rsvp_mendhi = rsvp_value
                
                if member.invited_vidhi:
                    rsvp_value = request.POST.get(f'rsvp_vidhi_{member_id}', 'pending')
                    member.rsvp_vidhi = rsvp_value
                
                if member.invited_wedding:
                    rsvp_value = request.POST.get(f'rsvp_wedding_{member_id}', 'pending')
                    member.rsvp_wedding = rsvp_value
                
                if member.invited_reception:
                    rsvp_value = request.POST.get(f'rsvp_reception_{member_id}', 'pending')
                    member.rsvp_reception = rsvp_value
                
                # Update dietary requirements
                member.dietary_requirements = request.POST.get(f'dietary_{member_id}', '')
                member.save()
            
            # Update family message
            family.message = request.POST.get('message', '')
            family.has_responded = True
            family.rsvp_submitted_at = timezone.now()
            family.save()
            
            rsvp_success = True
        except Exception as e:
            print(f"Error saving RSVP: {e}")
    
    # Get wedding info
    wedding_info = WeddingInfo.objects.first()
    if not wedding_info:
        wedding_info = {
            'partner1_name': 'Prit',
            'partner2_name': 'Khushboo',
        }
    
    # Organize members by event for display
    events_with_members = {
        'mendhi': {'details': event_details.get('mendhi', {}), 'members': [m for m in members if m.invited_mendhi]},
        'vidhi': {'details': event_details.get('vidhi', {}), 'members': [m for m in members if m.invited_vidhi]},
        'wedding': {'details': event_details.get('wedding', {}), 'members': [m for m in members if m.invited_wedding]},
        'reception': {'details': event_details.get('reception', {}), 'members': [m for m in members if m.invited_reception]},
    }
    
    context = {
        'family': family,
        'guest': family,  # Keep for backward compatibility
        'members': members,
        'events_with_members': events_with_members,
        'event_details': event_details,
        'rsvp_success': rsvp_success,
        'wedding_info': wedding_info,
    }
    return render(request, 'wedding/rsvp_form.html', context)


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with real-time RSVP tracking"""
    # Get all families (Guest objects)
    families = Guest.objects.all()
    total_families = families.count()
    
    # Get all family members
    members = FamilyMember.objects.all()
    total_members = members.count()
    
    # Response statistics (family level)
    responded = families.filter(has_responded=True).count()
    pending_families = families.filter(has_responded=False).count()
    
    # Per-event statistics from FamilyMember model
    events_stats = {
        'mendhi': {
            'invited': members.filter(invited_mendhi=True).count(),
            'attending': members.filter(invited_mendhi=True, rsvp_mendhi='attending').count(),
            'not_attending': members.filter(invited_mendhi=True, rsvp_mendhi='not_attending').count(),
            'pending': members.filter(invited_mendhi=True, rsvp_mendhi='pending').count(),
            'total_guests': members.filter(invited_mendhi=True, rsvp_mendhi='attending').count(),
        },
        'vidhi': {
            'invited': members.filter(invited_vidhi=True).count(),
            'attending': members.filter(invited_vidhi=True, rsvp_vidhi='attending').count(),
            'not_attending': members.filter(invited_vidhi=True, rsvp_vidhi='not_attending').count(),
            'pending': members.filter(invited_vidhi=True, rsvp_vidhi='pending').count(),
            'total_guests': members.filter(invited_vidhi=True, rsvp_vidhi='attending').count(),
        },
        'wedding': {
            'invited': members.filter(invited_wedding=True).count(),
            'attending': members.filter(invited_wedding=True, rsvp_wedding='attending').count(),
            'not_attending': members.filter(invited_wedding=True, rsvp_wedding='not_attending').count(),
            'pending': members.filter(invited_wedding=True, rsvp_wedding='pending').count(),
            'total_guests': members.filter(invited_wedding=True, rsvp_wedding='attending').count(),
        },
        'reception': {
            'invited': members.filter(invited_reception=True).count(),
            'attending': members.filter(invited_reception=True, rsvp_reception='attending').count(),
            'not_attending': members.filter(invited_reception=True, rsvp_reception='not_attending').count(),
            'pending': members.filter(invited_reception=True, rsvp_reception='pending').count(),
            'total_guests': members.filter(invited_reception=True, rsvp_reception='attending').count(),
        },
    }
    
    # Recent RSVPs (last 20 families)
    recent_rsvps = families.filter(has_responded=True).order_by('-rsvp_submitted_at')[:20]
    
    # Families who haven't responded
    pending_guests = families.filter(has_responded=False).order_by('name')
    
    context = {
        'total_guests': total_families,
        'total_members': total_members,
        'responded': responded,
        'pending': pending_families,
        'response_rate': round((responded / total_families * 100) if total_families > 0 else 0, 1),
        'events_stats': events_stats,
        'recent_rsvps': recent_rsvps,
        'pending_guests': pending_guests,
    }
    return render(request, 'wedding/admin_dashboard.html', context)


@staff_member_required
def admin_guest_list(request):
    """Admin view for full guest list with filtering"""
    guests = Guest.objects.all()
    
    # Filter by event
    event_filter = request.GET.get('event', '')
    if event_filter:
        if event_filter == 'mendhi':
            guests = guests.filter(invited_mendhi=True)
        elif event_filter == 'vidhi':
            guests = guests.filter(invited_vidhi=True)
        elif event_filter == 'wedding':
            guests = guests.filter(invited_wedding=True)
        elif event_filter == 'reception':
            guests = guests.filter(invited_reception=True)
    
    # Filter by RSVP status
    status_filter = request.GET.get('status', '')
    if status_filter == 'responded':
        guests = guests.filter(has_responded=True)
    elif status_filter == 'pending':
        guests = guests.filter(has_responded=False)
    elif status_filter == 'attending':
        guests = guests.filter(
            Q(rsvp_mendhi='attending') |
            Q(rsvp_vidhi='attending') |
            Q(rsvp_wedding='attending') |
            Q(rsvp_reception='attending')
        )
    elif status_filter == 'not_attending':
        guests = guests.filter(
            Q(rsvp_mendhi='not_attending') |
            Q(rsvp_vidhi='not_attending') |
            Q(rsvp_wedding='not_attending') |
            Q(rsvp_reception='not_attending')
        )
    
    # Search
    search = request.GET.get('search', '')
    if search:
        guests = guests.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(rsvp_code__icontains=search)
        )
    
    context = {
        'guests': guests,
        'event_filter': event_filter,
        'status_filter': status_filter,
        'search': search,
        'total_count': guests.count(),
    }
    return render(request, 'wedding/admin_guest_list.html', context)


@staff_member_required
def export_guests_csv(request):
    """Export guest list as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wedding_guests.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Email', 'Phone', 'Party Name', 'Max Guests', 'RSVP Code',
        'Invited Mendhi', 'Invited Vidhi', 'Invited Wedding', 'Invited Reception',
        'RSVP Mendhi', 'RSVP Vidhi', 'RSVP Wedding', 'RSVP Reception',
        'Guests Mendhi', 'Guests Vidhi', 'Guests Wedding', 'Guests Reception',
        'Dietary Requirements', 'Message', 'Has Responded', 'RSVP Submitted At'
    ])
    
    for guest in Guest.objects.all():
        writer.writerow([
            guest.name, guest.email, guest.phone, guest.party_name, guest.max_guests, guest.rsvp_code,
            guest.invited_mendhi, guest.invited_vidhi, guest.invited_wedding, guest.invited_reception,
            guest.rsvp_mendhi, guest.rsvp_vidhi, guest.rsvp_wedding, guest.rsvp_reception,
            guest.guests_mendhi, guest.guests_vidhi, guest.guests_wedding, guest.guests_reception,
            guest.dietary_requirements, guest.message, guest.has_responded, guest.rsvp_submitted_at
        ])
    
    return response


@staff_member_required  
@require_http_methods(["GET"])
def api_dashboard_stats(request):
    """API endpoint for real-time dashboard stats"""
    guests = Guest.objects.all()
    
    stats = {
        'total': guests.count(),
        'responded': guests.filter(has_responded=True).count(),
        'pending': guests.filter(has_responded=False).count(),
        'events': {
            'mendhi': {
                'attending': guests.filter(rsvp_mendhi='attending').aggregate(Sum('guests_mendhi'))['guests_mendhi__sum'] or 0,
            },
            'vidhi': {
                'attending': guests.filter(rsvp_vidhi='attending').aggregate(Sum('guests_vidhi'))['guests_vidhi__sum'] or 0,
            },
            'wedding': {
                'attending': guests.filter(rsvp_wedding='attending').aggregate(Sum('guests_wedding'))['guests_wedding__sum'] or 0,
            },
            'reception': {
                'attending': guests.filter(rsvp_reception='attending').aggregate(Sum('guests_reception'))['guests_reception__sum'] or 0,
            },
        },
        'recent': list(guests.filter(has_responded=True).order_by('-rsvp_submitted_at')[:5].values(
            'name', 'rsvp_submitted_at'
        ))
    }
    
    return JsonResponse(stats)
