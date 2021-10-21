from django.shortcuts import render

from .apps.blog import posts


def index(request):
    return render(request, 'home.html', context={'posts': posts.blog_posts})
