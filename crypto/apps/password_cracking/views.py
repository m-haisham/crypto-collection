from pathlib import Path

from django.shortcuts import render
from django.template.response import SimpleTemplateResponse

from .forms import DictionaryForm, BruteForm, HashForm
from .services import CrackingService
from django.contrib.staticfiles.storage import staticfiles_storage


def hash_word(request):
    form = HashForm(request.POST, request.FILES)

    if form.is_valid():
        word = form.cleaned_data.get('word')
        enc_type = form.cleaned_data.get('enc_type')

        service = CrackingService()

        context = {
            'hash': service.get_encryption_function(enc_type)(word.encode('utf-8')),
        }

        return SimpleTemplateResponse('password_cracking/hash-result.html', context)


def brute_crack(request):
    form = BruteForm(request.POST, request.FILES)

    if form.is_valid():

        hashed_word = form.cleaned_data.get('hashed_word')
        hashed_type = form.cleaned_data.get('enc_type')

        service = CrackingService()
        result = service.brute_force(hashed_word, 6, service.get_encryption_function(hashed_type))
        context = {
            "keyword": result.keyword,
            "is_cracked": result.is_cracked,
            'time_taken': result.time_taken,
            'processed_count': result.processed_count,
        }

        return SimpleTemplateResponse('password_cracking/response.html', context)
    else:
        return SimpleTemplateResponse('password_cracking/error_response.html', {'error': form.errors['hashed_word'][0]})


def dictionary(request):
    form = DictionaryForm(request.POST, request.FILES)

    # TODO default wordlist

    if form.is_valid():
        hashed_word = form.cleaned_data.get('hashed_word')
        enc_type = form.cleaned_data.get('enc_type')
        dict_file = form.cleaned_data.get('dict_file')
        if dict_file is None:
            dict_file = Path(staticfiles_storage.path('assets/wordlists/cewl_dvwa_password.txt'))

        def words():
            """return words of the file as a generator"""
            with dict_file.open('rb') as f:
                lines = f.read().split(b'\n')

            for line in lines:
                yield line

        service = CrackingService()
        result = service.crack(hashed_word, words(), service.get_encryption_function(enc_type))

        context = {
            "keyword": result.keyword,
            "is_cracked": result.is_cracked,
            'time_taken': result.time_taken,
            'processed_count': result.processed_count,
        }

        return SimpleTemplateResponse('password_cracking/response.html', context)
    else:
        return SimpleTemplateResponse('password_cracking/error_response.html', {'error': form.errors['hashed_word'][0]})


def cracking_renderer(request, context):
    context = {
        **context,
        'hform': HashForm(),
        'bform': BruteForm(),
        'dform': DictionaryForm(),
    }

    return render(request, 'posts/2021-07-14/password_cracking.html', context)
