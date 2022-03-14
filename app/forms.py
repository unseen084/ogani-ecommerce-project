from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation


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


class ProfileEditForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name', max_length=12, min_length=4, required=False,
                                 help_text='Required: First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=12, min_length=4, required=False,
                                help_text='Required: Last Name',
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    country = forms.CharField(label='Country', required=False, help_text='Required: Country',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    address = forms.CharField(label='Address', required=False, help_text='Required: Address',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(label='City', required=False, help_text='Required: City',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    postal_code = forms.CharField(label='Postal Code', required=False, help_text='Required: Zip Code',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17,
                                   required=False)  # validators should be a list
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'country', 'address', 'city', 'postal_code', 'phone_number', 'email']

    #class Meta:
    #    model = User
    #    labels = {'email': 'Email'}
    #    widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}
    #    fields = ['username', 'first_name', 'last_name', 'country', 'address', 'city', 'postal_code', 'phone_number', 'password1', 'password2', 'email']


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"),
                               strip=False,
                               widget=forms.TextInput(attrs={'autocomplete': 'current-password',
                                                             'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                                            'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
