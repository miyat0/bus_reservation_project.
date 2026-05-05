import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from staff.models import Staff
from admins.models import Bus

# Create Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created (pass: admin123)")

# Create Staff
if not User.objects.filter(username='staff').exists():
    staff_user = User.objects.create_user('staff', 'staff@example.com', 'staff123')
    staff_user.is_staff = True
    staff_user.save()
    Staff.objects.create(user=staff_user, contact_number='1234567890')
    print("Staff user 'staff' created (pass: staff123)")

# Create a sample Bus if none exists
if not Bus.objects.exists():
    Bus.objects.create(
        bus_name="Express 101",
        source="New York",
        destination="Boston",
        total_seats=40,
        available_seats=40,
        price=50
    )
    print("Sample bus 'Express 101' created")
