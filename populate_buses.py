import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admins.models import Bus
from django.contrib.auth.models import User
from staff.models import Staff

cities = [
    'Alappuzha', 'Ernakulam / Kochi', 'Kannur', 'Kottayam', 'Kozhikode', 'Munnar', 'Palakkad', 'Thiruvananthapuram', 'Thrissur', 'Wayanad',
    'Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli', 'Ooty', 'Kanyakumari', 'Vellore',
    'Bengaluru', 'Mysuru', 'Mangaluru', 'Hubballi', 'Belagavi', 'Udupi', 'Gokarna'
]

def create_test_users():
    # 1. Create Admin (admin/admin)
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin")
        print("Successfully created Admin user: admin / admin")
    else:
        print("Admin user already exists.")

    # 2. Create Staff (staff/staff)
    if not User.objects.filter(username="staff").exists():
        staff_user = User.objects.create_user("staff", "staff@example.com", "staff", is_staff=True)
        Staff.objects.get_or_create(user=staff_user, defaults={"contact_number": "9876543210"})
        print("Successfully created Staff user: staff / staff")
    else:
        print("Staff user already exists.")

    # 3. Create regular Traveler (user/user)
    if not User.objects.filter(username="user").exists():
        User.objects.create_user("user", "user@example.com", "user")
        print("Successfully created Regular User: user / user")
    else:
        print("Regular User already exists.")

def populate_buses():
    if Bus.objects.exists():
        print("Buses already exist in the database. Skipping bus seeding.")
        return
    
    bus_names = [
        "Kerala Express", "Tamil Nadu Voyager", "Karnataka Shuttle", "Telangana Link", 
        "South Star", "Deccan Queen", "Coastal Rider", "Highland Flyer", 
        "Metro Connect", "Heritage Transit", "Swift Silver", "Night Crawler"
    ]

    for i in range(15): # Add 15 buses
        name = f"{random.choice(bus_names)} {random.randint(100, 999)}"
        # Ensure unique names (primitive check)
        while Bus.objects.filter(bus_name=name).exists():
            name = f"{random.choice(bus_names)} {random.randint(100, 999)}"
            
        src = random.choice(cities)
        dest = random.choice([c for c in cities if c != src])
        
        seats = random.randint(30, 50)
        price = random.randint(500, 2500)
        
        # Departure between tomorrow and 7 days from now
        departure = timezone.now() + timedelta(days=random.randint(1, 7), hours=random.randint(0, 23))
        arrival = departure + timedelta(hours=random.randint(4, 12))
        
        Bus.objects.create(
            bus_name=name,
            source=src,
            destination=dest,
            total_seats=seats,
            available_seats=seats,
            price=price,
            departure_time=departure,
            arrival_time=arrival
        )
    print("Successfully added 15 South Indian bus routes.")

def populate():
    create_test_users()
    populate_buses()

if __name__ == "__main__":
    populate()
