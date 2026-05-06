from django.db import models
from django.contrib.auth.models import User
from admins.models import Bus

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10, blank=True)
    assigned_bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
