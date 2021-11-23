from collections import namedtuple

from django.shortcuts import render

from .apps.blog import posts

Contributor = namedtuple('Contributor', 'id name alias description profile thumbnail')

contributors = [
    Contributor(
        id='S1900884',
        name='Maadh',
        alias='maadhmohamed',
        description='</>.',
        profile='https://github.com/maadhmohamed',
        thumbnail='https://avatars.githubusercontent.com/u/44810382?v=4',
    ),
]


def index(request):
    return render(request, 'home.html', context={'posts': posts.blog_posts})


def about(request):
    return render(request, 'about.html', context={'contributors': contributors})
