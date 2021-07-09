from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse

from crypto.apps.hamming.services.hamming_code_service import HammingCodeService


def index(request):
    return render(request, "hamming/index.html")


def encode(request):
    service = HammingCodeService()
    sequence = request.POST['sequence']

    return TemplateResponse(request, 'hamming/encoded.html', context={'code': service.encode(sequence)})
