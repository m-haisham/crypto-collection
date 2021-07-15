import hashlib

from django.shortcuts import render
from django.template.response import SimpleTemplateResponse

from .services import CrackingService


def brute_force(request):
    context = {
        'hash_types': CrackingService.encryption_types,
    }

    return render(request, 'password_cracking/brute_force.html', context)


def brute_crack(request):
    hashed_word = request.POST['hash']
    hashed_type = request.POST['encryption']

    service = CrackingService()
    result = service.brute_force(hashed_word, 6, service.get_encryption_function(hashed_type))
    context = {
        "keyword": result.keyword,
        "is_cracked": result.is_cracked,
        'time_taken': result.time_taken,
        'processed_count': result.processed_count,
    }

    return SimpleTemplateResponse('password_cracking/brute_force_response.html', context)


def dictionary(request):
    return render(request, 'password_cracking/dictionary.html')