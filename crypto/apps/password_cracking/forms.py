from django import forms
from django.core import validators

from .services import CrackingService, hash_regex


class HashForm(forms.Form):
    word = forms.CharField()
    enc_type = forms.ChoiceField(choices=(((v, v) for v in CrackingService.encryption_types)))


class BruteForm(forms.Form):
    hashed_word = forms.CharField(validators=[
        validators.RegexValidator(hash_regex, message='Hash contains illegal characters.')]
    )

    enc_type = forms.ChoiceField(choices=(((v, v) for v in CrackingService.encryption_types)))


class DictionaryForm(forms.Form):
    hashed_word = forms.CharField(validators=[
        validators.RegexValidator(hash_regex, message='Hash contains illegal characters.')]
    )

    dict_file = forms.FileField(required=False)
    enc_type = forms.ChoiceField(choices=(((v, v) for v in CrackingService.encryption_types)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # always selected first choice
        self.initial['enc_type'] = CrackingService.encryption_types[0], CrackingService.encryption_types[0]
