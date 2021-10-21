from django import forms


class CCGenerateForm(forms.Form):
    issuer = forms.ChoiceField()
