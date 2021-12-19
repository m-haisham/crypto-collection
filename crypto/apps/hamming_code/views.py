from django.template.response import SimpleTemplateResponse

from . import services as service


def encode(request):
    sequence = request.POST['sequence'][::-1]

    if len(sequence) < 4:
        return SimpleTemplateResponse(
            'hamming_code/error.html', {'error': 'The binary sequence must have length greater than or equal to 4'})

    context = {
        'even': service.encode(sequence, True)[::-1],
        'odd': service.encode(sequence, False)[::-1],
    }

    return SimpleTemplateResponse('hamming_code/encoded.html', context)


def decode(request):
    sequence = request.POST['sequence'][::-1]
    is_even = request.POST['check'] == 'even'

    if len(sequence) < 7:
        return SimpleTemplateResponse(
            'hamming_code/error.html', {'error': 'The binary sequence must have length greater than or equal to 7'})

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

    return SimpleTemplateResponse('hamming_code/decoded.html', context)
