from urllib.parse import quote

from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
from django.templatetags.static import static

from .forms import CCGenerateForm, CCValidateForm
from .models import CreditCard
from .service import validate_credit_card, CreditCardService


def check(request):
    form = CCValidateForm(request.POST, request.FILES)

    if form.is_valid():
        sequence = form.cleaned_data.get('card_number')

        pk = CreditCardService.identify_type(sequence)
        if pk is None:
            card = CreditCard(name='unknown', thumbnail_link='assets/credit_cards/unknown.png')
        else:
            card = CreditCard.objects.get(pk=pk)

        personal, checksum = CreditCardService.user_identifier(sequence)

        context = {
            'valid': validate_credit_card(sequence),
            'card_number': sequence,
            'card_system': CreditCardService.identify_system(sequence),
            'card_type': card.name,
            'card_thumbnail': static(
                card.thumbnail_link) if card.thumbnail_link else f'https://via.placeholder.com/202x122?text={quote(card.name)}',
            'card_personal': personal,
            'card_checksum': checksum,
        }

        return SimpleTemplateResponse('luhn_algorithm/check_result.html', context)
    else:
        return SimpleTemplateResponse('luhn_algorithm/error.html', {'error': form.errors['card_number'][0]})


def generate(request):
    issuer = int(request.POST['issuer'])

    try:
        card = CreditCard.objects.get(pk=issuer)
    except CreditCard.DoesNotExist:
        return SimpleTemplateResponse('luhn_algorithm/generate_error.html', {'msg': 'Credit card issuer not found.'})

    context = {
        'card_number': CreditCardService.generate_card_number(issuer),
        'card_type': card.name,
        'card_thumbnail': static(
            card.thumbnail_link) if card.thumbnail_link else f'https://via.placeholder.com/202x122?text={quote(card.name)}',
    }

    return SimpleTemplateResponse('luhn_algorithm/generate_result.html', context)


def luhn(request, context):
    gform = CCGenerateForm()
    gform.fields['issuer'].choices = [(card.pk, card.name) for card in CreditCard.objects.all()]

    context = {
        **context,
        'gform': gform,
        'vform': CCValidateForm(),
    }

    return render(request, 'posts/2021-07-12/luhn_algorithm.html', context)
