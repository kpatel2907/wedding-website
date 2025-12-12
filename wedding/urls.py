from django.urls import path
from . import views

app_name = 'wedding'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('rsvp/', views.rsvp_lookup, name='rsvp_lookup'),
    path('rsvp/forgot-code/', views.forgot_code, name='forgot_code'),
    path('rsvp/forgot-code/sent/', views.forgot_code_sent, name='forgot_code_sent'),
    path('rsvp/<str:rsvp_code>/', views.rsvp_form, name='rsvp_form'),
    
    # Admin dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/guests/', views.admin_guest_list, name='admin_guest_list'),
    path('dashboard/export/', views.export_guests_csv, name='export_guests_csv'),
    path('api/dashboard/stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
]
