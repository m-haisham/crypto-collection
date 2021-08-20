from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('2021-07-14/brute-force-attack', views.brute, name='brute'),
    path('2021-07-17/dictionary-attack', views.dictionary, name='dictionary'),
    path('<str:date>/<str:name>', views.posts, name='posts'),
]
