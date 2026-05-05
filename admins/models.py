from django.db import models

class Bus(models.Model):
    bus_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    price = models.IntegerField()
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.bus_name