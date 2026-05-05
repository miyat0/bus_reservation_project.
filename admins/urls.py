from django.urls import path
from . import views

urlpatterns = [
    path('', views.bus_list, name='bus_list'),
    path('bus/add/', views.add_bus, name='add_bus'),
    path('bus/edit/<int:bus_id>/', views.edit_bus, name='edit_bus'),
    path('bus/delete/<int:bus_id>/', views.delete_bus, name='delete_bus'),
    path('all-bookings/', views.all_bookings, name='all_bookings'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('all-users/', views.all_users, name='all_users'),
    path('user/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('manage-staff/', views.manage_staff, name='manage_staff'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('discounts/', views.discount_offers, name='discount_offers'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reports/', views.admin_reports, name='admin_reports'),
    path('settings/', views.admin_settings, name='admin_settings'),
    path('profile/', views.admin_profile, name='admin_profile'),
]
