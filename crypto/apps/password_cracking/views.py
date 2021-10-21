from django.template.response import SimpleTemplateResponse

from .forms import DictionaryForm
from .services import CrackingService, validate_hash


def brute_crack(request):
    hashed_word = request.POST['hash']
    hashed_type = request.POST['encryption']

    if not validate_hash(hashed_word):
        return SimpleTemplateResponse(
            'password_cracking/error_response.html', {'error': 'The provided hash is invalid.'})

    service = CrackingService()
    result = service.brute_force(hashed_word, 6, service.get_encryption_function(hashed_type))
    context = {
        "keyword": result.keyword,
        "is_cracked": result.is_cracked,
        'time_taken': result.time_taken,
        'processed_count': result.processed_count,
    }

    return SimpleTemplateResponse('password_cracking/response.html', context)


def dictionary(request):
    form = DictionaryForm(request.POST, request.FILES)

    # TODO default wordlist

    if form.is_valid():
        hashed_word = form.cleaned_data['hashed_word']
        enc_type = form.cleaned_data['enc_type']
        dict_file = form.cleaned_data['dict_file']

        if not validate_hash(hashed_word):
            return SimpleTemplateResponse(
                'password_cracking/error_response.html', {'error': 'The provided hash is invalid.'})

        def words():
            """return words of the file as a generator"""
            with dict_file.open('r') as f:
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
