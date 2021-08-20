from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist


def posts(request, date: str, name: str):
    if '_' in f'{date}{name}':
        return redirect(f'/blog/{date}/{name}'.replace('_', '-'))

    try:
        return render(request, f'posts/{date}/{name.replace("-", "_")}.html')
    except TemplateDoesNotExist:
        raise Http404
