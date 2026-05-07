from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Bus
from users.models import Booking
from staff.models import Staff
from django import forms

class BusForm(forms.ModelForm):
    REGIONAL_CITIES = [
        # --- Kerala ---
        ('Alappuzha', 'Alappuzha (Kerala)'),
        ('Ernakulam / Kochi', 'Ernakulam / Kochi (Kerala)'),
        ('Kannur', 'Kannur (Kerala)'),
        ('Kottayam', 'Kottayam (Kerala)'),
        ('Kozhikode', 'Kozhikode (Kerala)'),
        ('Munnar', 'Munnar (Kerala)'),
        ('Palakkad', 'Palakkad (Kerala)'),
        ('Thiruvananthapuram', 'Thiruvananthapuram (Kerala)'),
        ('Thrissur', 'Thrissur (Kerala)'),
        ('Wayanad', 'Wayanad (Kerala)'),
        
        # --- Tamil Nadu ---
        ('Chennai', 'Chennai (Tamil Nadu)'),
        ('Coimbatore', 'Coimbatore (Tamil Nadu)'),
        ('Madurai', 'Madurai (Tamil Nadu)'),
        ('Salem', 'Salem (Tamil Nadu)'),
        ('Tiruchirappalli', 'Tiruchirappalli (Tamil Nadu)'),
        ('Ooty', 'Ooty (Tamil Nadu)'),
        ('Kanyakumari', 'Kanyakumari (Tamil Nadu)'),
        ('Vellore', 'Vellore (Tamil Nadu)'),
        
        # --- Karnataka ---
        ('Bengaluru', 'Bengaluru (Karnataka)'),
        ('Mysuru', 'Mysuru (Karnataka)'),
        ('Mangaluru', 'Mangaluru (Karnataka)'),
        ('Hubballi', 'Hubballi (Karnataka)'),
        ('Belagavi', 'Belagavi (Karnataka)'),
        ('Udupi', 'Udupi (Karnataka)'),
        ('Gokarna', 'Gokarna (Karnataka)'),
    ]

    source = forms.ChoiceField(
        choices=REGIONAL_CITIES,
        widget=forms.Select(attrs={'class': 'input', 'style': 'padding-left: 44px; height: 50px;'})
    )
    destination = forms.ChoiceField(
        choices=REGIONAL_CITIES,
        widget=forms.Select(attrs={'class': 'input', 'style': 'padding-left: 44px; height: 50px;'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fetch unique cities for suggestions
        sources = Bus.objects.values_list('source', flat=True).distinct()
        destinations = Bus.objects.values_list('destination', flat=True).distinct()
        self.cities = sorted(list(set(list(sources) + list(destinations))))

    class Meta:
        model = Bus
        fields = '__all__'

    def clean_bus_name(self):
        bus_name = self.cleaned_data.get('bus_name')
        # Check for duplicate names, excluding the current instance when editing
        if Bus.objects.filter(bus_name=bus_name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A fleet with this name already exists. Please use a unique name.")
        return bus_name

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total_seats')
        available = cleaned_data.get('available_seats')

        if total is not None and available is not None:
            if available > total:
                self.add_error('available_seats', "Available seats cannot exceed the total seat capacity.")
        return cleaned_data

class StaffAssignmentForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['assigned_bus']

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_staff:
            return redirect('staff_dashboard')
        else:
            return redirect('user_dashboard')
            
    # Dynamically fetch unique cities from existing fleet data
    sources = Bus.objects.values_list('source', flat=True).distinct()
    destinations = Bus.objects.values_list('destination', flat=True).distinct()
    cities = sorted(list(set(list(sources) + list(destinations))))
    
    from datetime import date
    return render(request, 'admins/home.html', {
        'cities': cities,
        'today_date': date.today().strftime('%Y-%m-%d')
    })

def bus_list(request):
    buses_list = Bus.objects.all().order_by('id')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    if source:
        buses_list = buses_list.filter(source__icontains=source)
    if destination:
        buses_list = buses_list.filter(destination__icontains=destination)
    
    paginator = Paginator(buses_list, 10)
    page_number = request.GET.get('page')
    buses = paginator.get_page(page_number)
    return render(request, 'admins/bus_list.html', {'buses': buses})

def add_bus(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('add_bus')
    else:
        form = BusForm()
    return render(request, 'admins/bus_form.html', {'form': form, 'title': 'Add New Service'})

def edit_bus(request, bus_id):
    if not request.user.is_staff: return HttpResponseForbidden()
    try:
        bus = Bus.objects.get(id=bus_id)
    except Bus.DoesNotExist:
        messages.warning(request, 'This service has already been removed or does not exist.')
        return redirect('bus_list')
    
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('bus_list')
    else:
        form = BusForm(instance=bus)
    return render(request, 'admins/bus_form.html', {'form': form, 'title': 'Edit Service'})

def delete_bus(request, bus_id):
    if not request.user.is_staff: return HttpResponseForbidden()
    try:
        bus = Bus.objects.get(id=bus_id)
    except Bus.DoesNotExist:
        messages.warning(request, 'This service has already been removed or does not exist.')
        return redirect('bus_list')
    
    if request.method == 'POST':
        bus_name = bus.bus_name
        bus.delete()
        messages.success(request, f'Service {bus_name} removed successfully.')
        return redirect('bus_list')
    return render(request, 'admins/confirm_delete.html', {'object': bus, 'type': 'Service'})

def all_bookings(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    bookings_list = Booking.objects.all().order_by('-booking_date')
    paginator = Paginator(bookings_list, 10)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)
    return render(request, 'admins/all_bookings.html', {'bookings': bookings})

def all_users(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    users_list = User.objects.all().order_by('-date_joined')
    
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    staff_members = Staff.objects.all()
    buses = Bus.objects.all()
    return render(request, 'admins/all_users.html', {'users': users, 'staff_members': staff_members, 'buses': buses})

def admin_reports(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    return render(request, 'admins/placeholder.html', {'title': 'Operational Reports'})

def admin_settings(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    return render(request, 'admins/placeholder.html', {'title': 'System Settings'})

def admin_profile(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    return render(request, 'admins/profile.html', {'user': request.user})

def toggle_user_status(request, user_id):
    if not request.user.is_staff: return HttpResponseForbidden()
    user = get_object_or_404(User, id=user_id)
    if user != request.user: # Don't block yourself
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f"User {user.username} {'activated' if user.is_active else 'blocked'}.")
    return redirect('all_users')

def delete_user(request, user_id):
    if not request.user.is_staff: return HttpResponseForbidden()
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own administrative account.")
        return redirect('all_users')
    
    if request.method == 'POST':
        user_name = user.username
        user.delete()
        messages.success(request, f'User {user_name} has been permanently removed.')
        return redirect('all_users')
    return render(request, 'admins/confirm_delete.html', {'object': user, 'type': 'User'})

def manage_staff(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    staff_members = Staff.objects.all()
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        bus_id = request.POST.get('bus_id')
        staff = get_object_or_404(Staff, id=staff_id)
        if bus_id:
            bus = get_object_or_404(Bus, id=bus_id)
            staff.assigned_bus = bus
        else:
            staff.assigned_bus = None
        staff.save()
        messages.success(request, f'Updated assignment for {staff.user.username}')
        return redirect('manage_staff')
        
    buses = Bus.objects.all()
    return render(request, 'admins/manage_staff.html', {'staff_members': staff_members, 'buses': buses})

def add_staff(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('contact_number')
        bus_id = request.POST.get('bus_id')
        
        if contact and len(contact) > 10:
            messages.error(request, 'Contact number cannot exceed 10 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            
            staff = Staff.objects.create(user=user, contact_number=contact)
            if bus_id:
                staff.assigned_bus = Bus.objects.get(id=bus_id)
                staff.save()
            
            messages.success(request, f'Staff member {username} created successfully.')
            return redirect('all_users')
            
    buses = Bus.objects.all()
    return render(request, 'admins/staff_form.html', {'buses': buses})

def admin_dashboard(request):
    if not request.user.is_staff: return HttpResponseForbidden()
    
    status_filter = request.GET.get('status')
    bookings = Booking.objects.all().order_by('-booking_date')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    buses_count = Bus.objects.count()
    bookings_count = Booking.objects.count()
    users_count = User.objects.count()
    staff_count = Staff.objects.count()
    
    # Simple analytics
    recent_bookings = bookings[:5]
    
    context = {
        'buses_count': buses_count,
        'bookings_count': bookings_count,
        'users_count': users_count,
        'staff_count': staff_count,
        'recent_bookings': recent_bookings,
        'current_status': status_filter or 'All',
    }
    return render(request, 'admins/dashboard.html', context)

def delete_booking(request, booking_id):
    if not request.user.is_staff: return HttpResponseForbidden()
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking removed successfully.')
        # Safely redirect back to referer or default to dashboard
        referer = request.META.get('HTTP_REFERER', '')
        if 'booking/delete' in referer or not referer:
            return redirect('admin_dashboard')
        return redirect(referer)
    return render(request, 'admins/confirm_delete.html', {'object': booking, 'type': 'Booking'})

