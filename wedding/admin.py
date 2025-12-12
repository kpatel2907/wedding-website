from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from .models import Event, StoryMilestone, RSVP, WeddingInfo, Guest


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'date', 'time', 'venue_name', 'is_featured', 'order']
    list_editable = ['order', 'is_featured']
    list_filter = ['is_featured', 'date']
    search_fields = ['name', 'venue_name']
    ordering = ['order', 'date']


@admin.register(StoryMilestone)
class StoryMilestoneAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order']
    list_editable = ['order']
    ordering = ['order']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'rsvp_code_display', 'party_size', 'invited_events_display', 
        'response_status', 'rsvp_summary_display', 'rsvp_submitted_at'
    ]
    list_filter = [
        'has_responded', 
        'invited_mendhi', 'invited_vidhi', 'invited_wedding', 'invited_reception',
        'rsvp_mendhi', 'rsvp_vidhi', 'rsvp_wedding', 'rsvp_reception'
    ]
    search_fields = ['name', 'email', 'rsvp_code', 'party_name']
    readonly_fields = ['id', 'rsvp_code', 'created_at', 'updated_at', 'rsvp_submitted_at', 'last_viewed_at']
    ordering = ['name']
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('name', 'email', 'phone', 'party_name', 'max_guests')
        }),
        ('RSVP Code', {
            'fields': ('rsvp_code',),
            'description': 'This unique code is automatically generated and used by the guest to access their invitation.'
        }),
        ('Event Invitations', {
            'fields': ('invited_mendhi', 'invited_vidhi', 'invited_wedding', 'invited_reception'),
            'description': 'Select which events this guest is invited to.'
        }),
        ('RSVP Responses', {
            'fields': (
                ('rsvp_mendhi', 'guests_mendhi'),
                ('rsvp_vidhi', 'guests_vidhi'),
                ('rsvp_wedding', 'guests_wedding'),
                ('rsvp_reception', 'guests_reception'),
            ),
        }),
        ('Additional Information', {
            'fields': ('dietary_requirements', 'message', 'notes'),
            'classes': ('collapse',)
        }),
        ('Status & Timestamps', {
            'fields': ('has_responded', 'rsvp_submitted_at', 'last_viewed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_invited_all_events', 'mark_invited_wedding_only', 'regenerate_rsvp_codes', 'export_selected_csv']
    
    def rsvp_code_display(self, obj):
        return format_html(
            '<code style="background: linear-gradient(135deg, #b8860b, #d4a853); color: white; padding: 8px 14px; border-radius: 6px; font-size: 14px; font-weight: bold; letter-spacing: 2px; display: inline-block;">{}</code>',
            obj.rsvp_code
        )
    rsvp_code_display.short_description = 'RSVP Code'
    rsvp_code_display.admin_order_field = 'rsvp_code'
    
    def party_size(self, obj):
        return obj.max_guests
    party_size.short_description = 'Party Size'
    
    def invited_events_display(self, obj):
        events = []
        if obj.invited_mendhi:
            events.append('M')
        if obj.invited_vidhi:
            events.append('V')
        if obj.invited_wedding:
            events.append('W')
        if obj.invited_reception:
            events.append('R')
        return ' | '.join(events) if events else '-'
    invited_events_display.short_description = 'Invited'
    
    def response_status(self, obj):
        if obj.has_responded:
            return format_html('<span style="color: green;">✓ Responded</span>')
        return format_html('<span style="color: orange;">⏳ Pending</span>')
    response_status.short_description = 'Status'
    
    def rsvp_summary_display(self, obj):
        parts = []
        if obj.invited_mendhi:
            color = 'green' if obj.rsvp_mendhi == 'attending' else ('red' if obj.rsvp_mendhi == 'not_attending' else 'gray')
            count = f'({obj.guests_mendhi})' if obj.rsvp_mendhi == 'attending' else ''
            parts.append(f'<span style="color:{color}">M{count}</span>')
        if obj.invited_vidhi:
            color = 'green' if obj.rsvp_vidhi == 'attending' else ('red' if obj.rsvp_vidhi == 'not_attending' else 'gray')
            count = f'({obj.guests_vidhi})' if obj.rsvp_vidhi == 'attending' else ''
            parts.append(f'<span style="color:{color}">V{count}</span>')
        if obj.invited_wedding:
            color = 'green' if obj.rsvp_wedding == 'attending' else ('red' if obj.rsvp_wedding == 'not_attending' else 'gray')
            count = f'({obj.guests_wedding})' if obj.rsvp_wedding == 'attending' else ''
            parts.append(f'<span style="color:{color}">W{count}</span>')
        if obj.invited_reception:
            color = 'green' if obj.rsvp_reception == 'attending' else ('red' if obj.rsvp_reception == 'not_attending' else 'gray')
            count = f'({obj.guests_reception})' if obj.rsvp_reception == 'attending' else ''
            parts.append(f'<span style="color:{color}">R{count}</span>')
        return format_html(' '.join(parts)) if parts else '-'
    rsvp_summary_display.short_description = 'RSVPs'
    
    @admin.action(description='Mark selected as invited to ALL events')
    def mark_invited_all_events(self, request, queryset):
        queryset.update(
            invited_mendhi=True,
            invited_vidhi=True,
            invited_wedding=True,
            invited_reception=True
        )
        self.message_user(request, f'{queryset.count()} guests marked as invited to all events.')
    
    @admin.action(description='Mark selected as invited to WEDDING & RECEPTION only')
    def mark_invited_wedding_only(self, request, queryset):
        queryset.update(
            invited_mendhi=False,
            invited_vidhi=False,
            invited_wedding=True,
            invited_reception=True
        )
        self.message_user(request, f'{queryset.count()} guests marked as invited to wedding & reception only.')
    
    @admin.action(description='Regenerate RSVP codes for selected')
    def regenerate_rsvp_codes(self, request, queryset):
        from .models import generate_rsvp_code
        for guest in queryset:
            new_code = generate_rsvp_code()
            while Guest.objects.filter(rsvp_code=new_code).exclude(pk=guest.pk).exists():
                new_code = generate_rsvp_code()
            guest.rsvp_code = new_code
            guest.save(update_fields=['rsvp_code'])
        self.message_user(request, f'Regenerated RSVP codes for {queryset.count()} guests.')


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'guests', 'submitted_at']
    list_filter = ['guests', 'submitted_at']
    search_fields = ['name', 'email']
    readonly_fields = ['submitted_at']
    date_hierarchy = 'submitted_at'


@admin.register(WeddingInfo)
class WeddingInfoAdmin(admin.ModelAdmin):
    list_display = ['partner1_name', 'partner2_name', 'wedding_date', 'location']
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


# Customize admin site
admin.site.site_header = "Wedding RSVP Administration"
admin.site.site_title = "Wedding Admin"
admin.site.index_title = "Wedding Management"
