from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('hamming-code/', include('crypto.apps.hamming.urls')),
    path('luhn-algorithm/', include('crypto.apps.luhn_algorithm.urls')),
    path('password-cracking/', include('crypto.apps.password_cracking.urls')),
    path('blog/', include('crypto.apps.blog.urls')),
]
