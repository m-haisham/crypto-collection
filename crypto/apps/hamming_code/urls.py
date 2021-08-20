from django.urls import path

from . import views

app_name = 'hamming'
urlpatterns = [
    path('encode/', views.encode, name='encode'),
    path('decode/', views.decode, name='decode'),
]
