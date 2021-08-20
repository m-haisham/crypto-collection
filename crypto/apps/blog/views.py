from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist

from crypto.apps.password_cracking.forms import DictionaryForm
from crypto.apps.password_cracking.services import CrackingService


def posts(request, date: str, name: str):
    if '_' in f'{date}{name}':
        return redirect(f'/blog/{date}/{name}'.replace('_', '-'))

    try:
        return render(request, f'posts/{date}/{name.replace("-", "_")}.html')
    except TemplateDoesNotExist:
        raise Http404


def brute(request):
    context = {
        'hash_types': CrackingService.encryption_types,
    }

    return render(request, 'posts/2021-07-14/brute_force_attack.html', context)


def dictionary(request):
    context = {
        'form': DictionaryForm(),
    }

    return render(request, 'posts/2021-07-17/dictionary_attack.html', context)
