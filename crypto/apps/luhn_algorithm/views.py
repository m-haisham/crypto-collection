from django.shortcuts import render
from django.template.response import SimpleTemplateResponse

from .models import CreditCard
from .service import LuhnAlgorithm, CreditCardService


def index(request):
    return render(request, 'luhn_algorithm/index.html')


def check(request):
    sequence = request.POST['card-number']

    pk = CreditCardService.identify_type(sequence)
    if pk is None:
        card = CreditCard(name='unknown', thumbnail_link='assets/credit_cards/unknown.png')
    else:
        card = CreditCard.objects.get(pk=pk)

    context = {
        'valid': LuhnAlgorithm.check_valid(sequence),
        'card_number': sequence,
        'card_system': CreditCardService.identify_system(sequence),
        'card_type': card.name,
        'card_thumbnail': card.thumbnail_link,
    }

    return SimpleTemplateResponse('luhn_algorithm/check_result.html', context)
