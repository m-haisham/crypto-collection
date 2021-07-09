from django.urls import path

from . import views

app_name = 'hamming'
urlpatterns = [
    path('', views.index, name='index'),
    path('encode/', views.encode, name='encode'),
]
