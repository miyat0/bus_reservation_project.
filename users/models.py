from django.db import models
from django.contrib.auth.models import User
from admins.models import Bus

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('In-progress', 'In-progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=100)
    number_of_seats = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_boarded = models.BooleanField(default=False)
    
    # New fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    notes = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.bus.bus_name} (Seat: {self.seat_number})"
