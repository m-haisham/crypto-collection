from django.urls import path

from . import views

app_name = 'password_cracking'
urlpatterns = [
    path('brute-crack/', views.brute_crack, name='brute_crack'),
    path('dictionary/', views.dictionary, name='dictionary'),
]
