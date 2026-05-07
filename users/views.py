from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden

from .models import Booking
from admins.models import Bus
from .forms import SignUpForm, BookingForm, ReviewForm

def signup_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login')
    return render(request, 'users/signup.html', {'form': form})

@login_required
def user_profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'users/profile.html', {'user': request.user, 'bookings': bookings})

@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related('bus').order_by('-booking_date')
    total_bookings = bookings.count()
    active_bookings = bookings.filter(status__in=['Confirmed', 'In-progress']).count()

    context = {
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'recent_bookings': bookings[:5],
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('bus').order_by('-booking_date')
    return render(request, 'users/my_bookings.html', {'bookings': bookings})

def search_buses(request):
    # Dynamically fetch unique cities from existing fleet data
    sources = Bus.objects.values_list('source', flat=True).distinct()
    destinations = Bus.objects.values_list('destination', flat=True).distinct()
    
    # Standard Indian cities as fallback
    default_cities = ['Kochi', 'Trivandrum', 'Kozhikode', 'Chennai', 'Coimbatore', 'Madurai', 'Bangalore', 'Mysore', 'Mangalore', 'Hyderabad']
    
    db_cities = list(set(list(sources) + list(destinations)))
    cities = sorted(list(set(db_cities + default_cities))) if not db_cities else sorted(db_cities)
    
    buses = Bus.objects.all().order_by('departure_time')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    travel_date = request.GET.get('travel_date')
    
    # If no date is searched, default to showing only future trips
    if not travel_date:
        buses = buses.filter(departure_time__gte=timezone.now())
    
    if source:
        buses = buses.filter(source__icontains=source)
    if destination:
        buses = buses.filter(destination__icontains=destination)
    if travel_date:
        buses = buses.filter(departure_time__date=travel_date)
        
    return render(request, 'users/search_buses.html', {
        'buses': buses,
        'current_time': timezone.now(),
        'cities': cities
    })

from django.utils import timezone

@login_required
def book_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    
    # Date Validation: Prevent booking past trips
    if bus.departure_time < timezone.now():
        messages.error(request, 'This journey has already departed. Please choose a future trip.')
        return redirect('search_buses')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.bus = bus
            
            # Handle multiple seat numbers from dynamic inputs
            seat_list = request.POST.getlist('seat_number')
            booking.seat_number = ", ".join(filter(None, seat_list))
            
            # Conflict Detection
            requested_seats = [s.strip() for s in booking.seat_number.split(',') if s.strip()]
            
            # Get all already booked seats for this bus
            existing_bookings = Booking.objects.filter(bus=bus, status='Confirmed')
            all_booked_seats = []
            for b in existing_bookings:
                all_booked_seats.extend([s.strip() for s in b.seat_number.split(',')])
            
            conflicts = [s for s in requested_seats if s in all_booked_seats]
            
            if not requested_seats:
                form.add_error('seat_number', 'Please provide at least one seat number.')
            elif len(requested_seats) != booking.number_of_seats:
                form.add_error('seat_number', f'You selected {booking.number_of_seats} seats but provided {len(requested_seats)} seat numbers.')
            elif booking.number_of_seats > bus.available_seats:
                form.add_error('number_of_seats', f'Only {bus.available_seats} seats available.')
            elif conflicts:
                form.add_error('seat_number', f"Seat(s) {', '.join(conflicts)} are already booked.")
            else:
                booking.save()
                bus.available_seats -= booking.number_of_seats
                bus.save()
                messages.success(request, f'Successfully booked seat(s): {booking.seat_number}!')
                return redirect('user_dashboard')
    else:
        form = BookingForm()
        
    return render(request, 'users/book_bus.html', {'form': form, 'bus': bus})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        if booking.status in ['Confirmed', 'In-progress']:
            booking.status = 'Cancelled'
            booking.save()
            
            bus = booking.bus
            bus.available_seats += booking.number_of_seats
            bus.save()
            messages.success(request, 'Booking cancelled successfully.')
        return redirect('user_dashboard')
    return HttpResponseForbidden()

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

@login_required
def review_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != 'Completed':
        messages.error(request, 'You can only review completed trips.')
        return redirect('user_dashboard')
        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submitted successfully.')
            return redirect('user_dashboard')
    else:
        form = ReviewForm(instance=booking)
        
    return render(request, 'users/review_booking.html', {'form': form, 'booking': booking})
