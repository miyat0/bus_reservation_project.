from django import template
from staff.models import Staff

register = template.Library()

@register.filter
def is_staff_member(user):
    if not user.is_authenticated:
        return False
    return Staff.objects.filter(user=user).exists()
