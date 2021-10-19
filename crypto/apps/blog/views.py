from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist

from crypto.apps.password_cracking.forms import DictionaryForm
from crypto.apps.password_cracking.services import CrackingService

from .posts import blog_posts, posts_index


def brute(request, context):
    context = {
        **context,
        'hash_types': CrackingService.encryption_types,
    }

    return render(request, 'posts/2021-07-14/brute_force_attack.html', context)


def dictionary(request, context):
    context = {
        **context,
        'form': DictionaryForm(),
    }

    return render(request, 'posts/2021-07-17/dictionary_attack.html', context)


unique_renderers = {
    ('2021-07-14', 'brute-force-attack'): brute,
    ('2021-07-17', 'dictionary-attack'): dictionary,
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
        'next': blog_posts[post_index + 1] if post_index <= len(blog_posts) else None,
    }

    try:
        return unique_renderers[(date, name)](request, context)
    except KeyError:
        pass

    try:
        return render(request, f'posts/{date}/{name.replace("-", "_")}.html', context)
    except TemplateDoesNotExist:
        raise Http404
