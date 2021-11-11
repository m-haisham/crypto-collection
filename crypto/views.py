from collections import namedtuple

from django.shortcuts import render

from .apps.blog import posts

Contributor = namedtuple('Contributor', 'id name alias description profile thumbnail')

contributors = [
    Contributor(
        id='S1901061',
        name='Haisham',
        alias='Mensch272',
        description='I am a human 🤥.',
        profile='https://github.com/mensch272',
        thumbnail='https://avatars.githubusercontent.com/u/47662901?v=4',
    ),
]


def index(request):
    return render(request, 'home.html', context={'posts': posts.blog_posts})


def about(request):
    return render(request, 'about.html', context={'contributors': contributors})
