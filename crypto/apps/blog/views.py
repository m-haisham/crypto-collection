from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist

from .posts import blog_posts, posts_index
from ..luhn_algorithm.views import luhn
from ..password_cracking.views import cracking_renderer

unique_renderers = {
    ('2021-07-12', 'luhn-algorithm'): luhn,
    ('2021-07-14', 'password-cracking'): cracking_renderer,
}


def posts(request, date: str, name: str):
    if '_' in f'{date}{name}':
        return redirect(f'/blog/{date}/{name}'.replace('_', '-'))

    try:
        post_index = posts_index[(date, name)]
    except KeyError:
        raise Http404

    context = {
        'current': blog_posts[post_index],
        'previous': blog_posts[post_index - 1] if post_index > 0 else None,
        'next': blog_posts[post_index + 1] if post_index <= len(blog_posts) - 2 else None,
    }

    try:
        return unique_renderers[(date, name)](request, context)
    except KeyError:
        pass

    try:
        return render(request, f'posts/{date}/{name.replace("-", "_")}.html', context)
    except TemplateDoesNotExist:
        raise Http404
