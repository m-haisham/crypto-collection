import re

from django import forms
from django.core import validators


class CCGenerateForm(forms.Form):
    issuer = forms.ChoiceField()


class CCValidateForm(forms.Form):
    number_regex = re.compile(r'^[0-9]+$')
    card_number = forms.CharField(
        min_length=12, max_length=20,
        validators=[validators.RegexValidator(number_regex, message='Credit card number contains illegal characters.')]
    )
