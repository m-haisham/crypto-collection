from django.shortcuts import render
from django.template.response import SimpleTemplateResponse

from .services import HammingService


def index(request):
    return render(request, "hamming/index.html")


def encode(request):
    service = HammingService()
    sequence = request.POST['sequence'][::-1]

    context = {
        'even': service.encode(sequence, True)[::-1],
        'odd': service.encode(sequence, False)[::-1],
    }

    return SimpleTemplateResponse('hamming/encoded.html', context)


def decode(request):
    service = HammingService()
    sequence = request.POST['sequence'][::-1]
    is_even = request.POST['check'] == 'even'

    correct, error_position = service.detect_error(sequence, is_even)
    data = service.decode(correct)

    context = {
        'has_error': error_position != 0,
        'error_position': error_position,
        'error_bit_label': service.bit_label(error_position),
        'original': sequence[::-1],
        'corrected': correct[::-1],
        'data': data[::-1],
    }

    return SimpleTemplateResponse('hamming/decoded.html', context)
