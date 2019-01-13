import re
from django import forms
from .models import (
    Company,
    Person,
    Retail,
    Offer,
    OfferRetail,
)

DATE_INPUT_FORMATS = ['%d-%m-%Y', '%d %m %Y', '%d/%m/%Y']


# model forms
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


class CompanyPersonCreateForm(PhoneEmailValidCreateForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput)

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


class CompanyRetailCreateForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput)
    drawing_number = forms.CharField(required=False)
    cutting_length = forms.IntegerField(required=False)
    cutting_time = forms.IntegerField(required=False)
    price = forms.DecimalField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)

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
            'description',
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


class CompanyOfferCreateForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput)
    final_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)

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


class OfferRetailCreateForm(forms.ModelForm):
    class Meta:
        model = OfferRetail
        fields = [
            'offer',
            'retail',
            'quantity',
        ]

    def __init__(self, *args, **kwargs):
        super(OfferRetailCreateForm, self).__init__(*args, **kwargs)
        if self.initial.get('offer'):
            offer = self.initial['offer']
            self.fields['retail'].queryset = Retail.objects.filter(
                company_id=offer.company_id).order_by('name', 'thickness')
            self.fields['offer'] = forms.ModelChoiceField(queryset=Offer.objects.all(), widget=forms.HiddenInput)
        else:
            retail = self.initial['retail']
            self.fields['offer'].queryset = Offer.objects.filter(company_id=retail.company_id).order_by('-id')
            self.fields['retail'] = forms.ModelChoiceField(queryset=Retail.objects.all(), widget=forms.HiddenInput)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        regex = r'^(\d)+$'
        if not re.fullmatch(regex, str(quantity)):
            raise forms.ValidationError('Quantity must be positive number')
        return quantity

    def clean(self):
        data = self.cleaned_data
        offerretail = OfferRetail.objects.filter(offer_id=data['offer'].id, retail_id=data['retail'].id)
        if offerretail:
            raise forms.ValidationError(f'{data["retail"]} already in {data["offer"]}')
        return data


class OfferRetailUpdateForm(forms.ModelForm):
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), widget=forms.HiddenInput)
    retail = forms.ModelChoiceField(queryset=Retail.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = OfferRetail
        fields = [
            'offer',
            'retail',
            'quantity',
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        regex = r'^(\d)+$'
        if not re.fullmatch(regex, str(quantity)):
            raise forms.ValidationError('Quantity must be positive number')
        return quantity


# search forms
class CompanySearchForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        fields = [
            'name',
            'email',
            'phone',
            'address',
        ]
