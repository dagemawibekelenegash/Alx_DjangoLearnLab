from django import forms
from django.core.validators import validate_email
from .forms import ExampleForm

class UserForm(forms.Form):
    email = forms.EmailField(validators=[validate_email])
