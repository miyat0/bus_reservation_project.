from django.contrib import admin
from django.urls import include, path

from admins.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('buses/', include('admins.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('staff/', include('staff.urls')),
]
