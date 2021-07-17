from django import forms

from .services import CrackingService


class DictionaryForm(forms.Form):
    hashed_word = forms.CharField()
    dict_file = forms.FileField()
    enc_type = forms.ChoiceField(choices=(((v, v) for v in CrackingService.encryption_types)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # always selected first choice
        self.initial['enc_type'] = CrackingService.encryption_types[0], CrackingService.encryption_types[0]
