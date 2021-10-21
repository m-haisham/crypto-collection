from django.urls import path

from . import views

app_name = 'luhn_algorithm'
urlpatterns = [
    path('check/', views.check, name='check'),
    path('generate/', views.generate, name='generate'),
]
