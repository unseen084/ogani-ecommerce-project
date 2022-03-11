from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=12, min_length=4, required=True, help_text='Required: First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=12, min_length=4, required=True, help_text='Required: Last Name',
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    country = forms.CharField(label='Country', required=True, help_text='Required: Country',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    address = forms.CharField(label='Address',required=True, help_text='Required: Address',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(label='City',required=True, help_text='Required: City',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    postal_code = forms.CharField(label='Postal Code',required=True, help_text='Required: Zip Code',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, required=True)  # validators should be a list
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}
        fields = ['username', 'first_name', 'last_name', 'country', 'address', 'city', 'postal_code', 'phone_number', 'password1', 'password2', 'email']
