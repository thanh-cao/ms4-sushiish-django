from django import forms

from checkout.forms import validate_phone_number
from .models import Address
from django.contrib.auth.models import User


class UserDetailsForm(forms.ModelForm):
    '''
    Form for creating and updating user details
    '''
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = True
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = placeholder


class AddressForm(forms.ModelForm):
    '''
    Form for creating and updating user addresses
    '''
    class Meta:
        model = Address
        fields = ['phone_number', 'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country', 'address_type',
                  'isDefault']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Postcode',
            'country': 'Country',
            'address_type': 'Address Type',
            'isDefault': 'Set default',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = True
            self.fields[field].label = labels[field]

        self.fields['country'].widget.attrs['readonly'] = True
        self.fields['phone_number'].validators.append(validate_phone_number)
