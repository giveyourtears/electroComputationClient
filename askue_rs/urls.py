from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('light/', include('light.urls')),
    path('accounting/', include('find_device.urls')),
    path('device/', include('device_info.urls')),
    path('res/', include('res.urls')),
    path('balance/', include('substation_info.urls')),
]
