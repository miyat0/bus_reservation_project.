from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='staff_dashboard'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('availability/', views.staff_availability, name='staff_availability'),
    path('schedule/', views.staff_schedule, name='staff_schedule'),
    path('update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('add-notes/<int:booking_id>/', views.add_booking_notes, name='add_booking_notes'),
    path('profile/', views.staff_profile, name='staff_profile'),
]
