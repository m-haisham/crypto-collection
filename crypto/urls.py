from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('hamming-code/', include('crypto.apps.hamming_code.urls')),
    path('luhn-algorithm/', include('crypto.apps.luhn_algorithm.urls')),
    path('password-cracking/', include('crypto.apps.password_cracking.urls')),
    path('blog/', include('crypto.apps.blog.urls')),
    path('chat/', include('crypto.apps.chat.urls')),
]
