from urllib.parse import quote

from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
from django.templatetags.static import static

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

    personal, checksum = CreditCardService.user_identifier(sequence)

    context = {
        'valid': LuhnAlgorithm.check_valid(sequence),
        'card_number': sequence,
        'card_system': CreditCardService.identify_system(sequence),
        'card_type': card.name,
        'card_thumbnail': static(card.thumbnail_link) if card.thumbnail_link else f'https://via.placeholder.com/202x122?text={quote(card.name)}',
        'card_personal': personal,
        'card_checksum': checksum,
    }

    return SimpleTemplateResponse('luhn_algorithm/check_result.html', context)
