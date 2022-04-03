from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, label='Email')

    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get('email')
        if first_name == "" and last_name == "":
            raise ValidationError('Name, Last Name must be filled')
        else:
            return cleaned_data
