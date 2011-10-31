from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class EmailAuthenticationForm(AuthenticationForm):
    """Email authentication Form
    increase the size of the username field to fit long emails"""
    # TODO: consider to change this to an email only field
    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput(attrs={'class': 'text'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(
                                   attrs={'class': 'text'}))
    remember_me = forms.BooleanField(label='Keep me logged in',
                                     required=False)
