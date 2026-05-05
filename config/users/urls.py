from django.urls import path

from .views import dashboard_view, my_bookings, signup_view, search_buses, book_bus, cancel_booking, review_booking, user_profile, change_password

urlpatterns = [
    path('dashboard/', dashboard_view, name='user_dashboard'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('signup/', signup_view, name='signup'),
    path('search/', search_buses, name='search_buses'),
    path('book/<int:bus_id>/', book_bus, name='book_bus'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('review/<int:booking_id>/', review_booking, name='review_booking'),
    path('profile/', user_profile, name='user_profile'),
    path('change-password/', change_password, name='change_password'),
]
