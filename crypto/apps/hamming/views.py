from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse

from crypto.apps.hamming.services.hamming_service import HammingService


def index(request):
    return render(request, "hamming/index.html")


def encode(request):
    service = HammingService()
    sequence = request.POST['sequence'][::-1]

    context = {
        'even': service.encode(sequence, True)[::-1],
        'odd': service.encode(sequence, False)[::-1],
    }

    return TemplateResponse(request, 'hamming/encoded.html', context)


def decode(request):
    service = HammingService()
    sequence = request.POST['sequence']
