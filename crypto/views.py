from collections import namedtuple

from django.shortcuts import render

from .apps.blog import posts

Contributor = namedtuple('Contributor', 'id name alias description profile thumbnail')

contributors = [
    Contributor(
        id='S1801024',
        name='Sahaf',
        alias='Codemachine0101',
        description='Connoisseur of Tamamo.',
        profile='https://github.com/Codemachine0101',
        thumbnail='https://avatars.githubusercontent.com/u/53483283?v=4',
    ),
]


def index(request):
    return render(request, 'home.html', context={'posts': posts.blog_posts})


def about(request):
    return render(request, 'about.html', context={'contributors': contributors})
