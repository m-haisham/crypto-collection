import hashlib

from django.shortcuts import render
from django.template.response import SimpleTemplateResponse

from .services import PasswordCrackingService


def brute_force(request):
    return render(request, 'password_cracking/brute_force.html')


def brute_crack(request):
    service = PasswordCrackingService()
    hashed_word = request.POST['hash']

    def encrypt(value):
        return hashlib.sha1(value.encode('utf-8')).hexdigest()

    result = service.brute_force(hashed_word, 6, encrypt)
    context = {
        "keyword": result.keyword,
        "is_cracked": result.is_cracked,
        'time_taken': result.time_taken,
        'processed_count': result.processed_count,
    }

    return SimpleTemplateResponse('password_cracking/brute_force_response.html', context)


def dictionary(request):
    return render(request, 'password_cracking/dictionary.html')
