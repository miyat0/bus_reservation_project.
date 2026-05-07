from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from .models import Staff
from users.models import Booking

@login_required
def dashboard(request):
    try:
        staff = request.user.staff
    except ObjectDoesNotExist:
        return redirect('home')
    
    assigned_bus = staff.assigned_bus
    passengers = []
    if assigned_bus:
        passengers = Booking.objects.filter(bus=assigned_bus)
    
    context = {
        'staff': staff,
        'assigned_bus': assigned_bus,
        'passengers': passengers
    }
    return render(request, 'staff/dashboard.html', context)

@login_required
def staff_schedule(request):
    try:
        staff = request.user.staff
    except ObjectDoesNotExist: return redirect('home')
    return render(request, 'staff/schedule.html', {'staff': staff})

@login_required
def staff_availability(request):
    try:
        staff = request.user.staff
    except ObjectDoesNotExist: return redirect('home')
    if request.method == 'POST':
        staff.is_available = not staff.is_available
        staff.save()
        messages.success(request, f"Availability updated to {'Free' if staff.is_available else 'Busy'}")
        return redirect('staff_availability')
    return render(request, 'staff/availability.html', {'staff': staff})

@login_required
def toggle_availability(request):
    # Keep for backward compatibility or simple toggle
    try:
        staff = request.user.staff
        staff.is_available = not staff.is_available
        staff.save()
    except ObjectDoesNotExist: pass
    return redirect('staff_dashboard')

@login_required
def staff_profile(request):
    return render(request, 'staff/profile.html', {'user': request.user, 'staff': getattr(request.user, 'staff', None)})

@login_required
def update_booking_status(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        if hasattr(request.user, 'staff') and request.user.staff.assigned_bus == booking.bus:
            new_status = request.POST.get('status')
            if new_status in dict(Booking.STATUS_CHOICES):
                booking.status = new_status
                booking.save()
                
                messages.success(request, f"Passenger {booking.user.username}'s status updated to {new_status}")

                # If status becomes cancelled, free the seat
                if new_status == 'Cancelled':
                    bus = booking.bus
                    bus.available_seats += 1
                    bus.save()
                    booking.delete()
                    messages.warning(request, "Booking cancelled and seat released.")
                    
        return redirect('staff_dashboard')
    return HttpResponseForbidden()

@login_required
def add_booking_notes(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        if hasattr(request.user, 'staff') and request.user.staff.assigned_bus == booking.bus:
            notes = request.POST.get('notes')
            booking.notes = notes
            booking.save()
            messages.success(request, f"Notes added for {booking.user.username}")
        return redirect('staff_dashboard')
    return HttpResponseForbidden()
