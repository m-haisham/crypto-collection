from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hamming/', include('crypto.apps.hamming.urls')),
    path('luhn-algorithm/', include('crypto.apps.luhn_algorithm.urls')),
]
