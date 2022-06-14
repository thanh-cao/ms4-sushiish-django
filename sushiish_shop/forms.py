from dataclasses import fields
from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    field_order = ['first_name', 'last_name', 'username',
                   'email', 'email2', 'password1', 'password2']

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user
