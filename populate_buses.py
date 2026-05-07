import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admins.models import Bus

cities = ['Kochi', 'Trivandrum', 'Kozhikode', 'Chennai', 'Coimbatore', 'Madurai', 'Bangalore', 'Mysore', 'Mangalore', 'Hyderabad']

def populate():
    if Bus.objects.exists():
        print("Buses already exist in the database. Skipping seeding.")
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

if __name__ == "__main__":
    populate()
