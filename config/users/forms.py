from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Booking

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat_number']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['rating', 'review']
