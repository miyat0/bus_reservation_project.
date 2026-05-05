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
    buses = Bus.objects.all()
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    
    if source:
        buses = buses.filter(source__icontains=source)
    if destination:
        buses = buses.filter(destination__icontains=destination)
        
    return render(request, 'users/search_buses.html', {'buses': buses})

@login_required
def book_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.bus = bus
            
            if booking.seat_number <= 0:
                form.add_error('seat_number', 'Seat number must be greater than 0.')
            elif bus.available_seats <= 0:
                form.add_error(None, 'No seats available on this bus.')
            else:
                booking.save()
                bus.available_seats -= 1
                bus.save()
                messages.success(request, 'Booking successful!')
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
            bus.available_seats += 1
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
