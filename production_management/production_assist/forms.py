import re
from django import forms
from .models import (
    Company,
    Person,
    Retail,
    Offer,
)

DATE_INPUT_FORMATS = ['%d-%m-%Y', '%d %m %Y', '%d/%m/%Y']


class PhoneEmailValidCreateForm(forms.ModelForm):
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


# COMPANY
class CompanyCreateForm(forms.ModelForm):
    name = forms.CharField(label='Company Name')

    class Meta:
        model = Company
        fields = [
            'name'
        ]


class CompanyUpdateForm(PhoneEmailValidCreateForm):
    email = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'phone',
            'email',
            'description',
        ]


# PERSON
class PersonCreateForm(PhoneEmailValidCreateForm):
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


class CompanyPersonCreateForm(PersonCreateForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput)


# RETAIL
class RetailCreateForm(forms.ModelForm):
    drawing_number = forms.CharField(required=False)
    cutting_length = forms.IntegerField(required=False)
    cutting_time = forms.IntegerField(required=False)
    price = forms.DecimalField(required=False)

    class Meta:
        model = Retail
        fields = [
            'company',
            'name',
            'drawing_number',
            'material',
            'thickness',
            'width',
            'length',
            'cutting_length',
            'cutting_time',
            'price',
        ]

    def clean(self):
        data = self.cleaned_data
        if data['width'] > data['length']:
            data['width'], data['length'] = data['length'], data['width']
        if not data['cutting_length']:
            data['cutting_length'] = 0
        if not data['cutting_time']:
            data['cutting_time'] = 0
        if not data['price']:
            data['price'] = 0
        return data


class CompanyRetailCreateForm(RetailCreateForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput)


# OFFER
class OfferCreateForm(forms.ModelForm):
    final_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = Offer
        fields = [
            'company',
            'status',
            'manufacture',
            'final_date',
        ]


class CompanyOfferCreateForm(OfferCreateForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Offer
        fields = [
            'company',
            'person',
            'status',
            'manufacture',
            'final_date',
        ]

    def __init__(self, *args, **kwargs):
        super(CompanyOfferCreateForm, self).__init__(*args, **kwargs)
        company = self.initial['company']
        self.fields['person'].queryset = Person.objects.filter(company=company)
