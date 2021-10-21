from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('<str:date>/<str:name>', views.posts, name='posts'),
]
