import re
from django import forms
from .models import (
    Company,
    Person,
)


class CompanyCreateForm(forms.ModelForm):
    name = forms.CharField(label='Company Name')

    class Meta:
        model = Company
        fields = [
            'name'
        ]


class CompanyUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Company Name')
    email = forms.CharField(label='Email', required=False, )
    phone = forms.CharField(label='Phone', required=False)
    address = forms.CharField(label='Address', required=False)

    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'phone',
            'email',
        ]

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone != '':
            regex = r'^(\+(\d){1,3}\s?)?((\d){3}\s?(\d){3}\s?(\d){3}$|(\d){2}\s?(\d){3}\s?(\d){2}\s?(\d){2})$'
            if not re.fullmatch(regex, phone):
                raise forms.ValidationError('Wrong format, try xxx xxx xxx or xx xxx xx xx')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != '':
            regex = r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]{1,})*\.([a-zA-Z]{2,}){1}$'
            if not re.fullmatch(regex, email):
                raise forms.ValidationError('Wrong email format')
        return email


class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'company',
            'first_name',
            'last_name',
            'phone',
            'email',
            'position',
        ]

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone != '':
            regex = r'^(\+(\d){1,3}\s?)?((\d){3}\s?(\d){3}\s?(\d){3}$|(\d){2}\s?(\d){3}\s?(\d){2}\s?(\d){2})$'
            if not re.fullmatch(regex, phone):
                raise forms.ValidationError('Wrong format, try xxx xxx xxx or xx xxx xx xx')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != '':
            regex = r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]{1,})*\.([a-zA-Z]{2,}){1}$'
            if not re.fullmatch(regex, email):
                raise forms.ValidationError('Wrong email format')
        return email


class PersonUpdateForm(PersonCreateForm):
    class Meta:
        model = Person
        exclude = ['company']
