from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ModifiedForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

        widgets = {
            'username': forms.TextInput(attrs={'class':'validate'}),
            'password1': forms.PasswordInput(attrs={'class':"validate"}),
            'password2': forms.PasswordInput(attrs={'class':"validate"})
        }