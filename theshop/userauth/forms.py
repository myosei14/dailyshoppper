from django import forms
from django.forms import ModelForm
from .models import Customer, AccountInfo


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'password']
        labels = {
            'name': 'First and last name'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First and last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }


class AccountInfoForm(ModelForm):
    class Meta:
        model = AccountInfo
        # fields = '__all__'
        fields = ['house_number', 'street', 'town', 'region_or_county', 'postcode', 'country', 'phone']
        # exclude = ['customer',]
        widgets = {
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'town': forms.TextInput(attrs={'class': 'form-control'}),
            'region_or_county': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            # 'customer': forms.HiddenInput(attrs={'value': 4}),
        }
