from django import forms


class ConfirmUsernameForm(forms.Form):
    username = forms.CharField(required=True)
