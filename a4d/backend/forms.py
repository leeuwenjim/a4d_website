from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=User._meta.get_field('username').max_length, required=True, label='Gebruikersnaam', widget=forms.TextInput(attrs={'placeholder': 'Gebruikersnaam'}))
    password = forms.CharField(max_length=User._meta.get_field('password').max_length, required=True, label='Wachtwoord', widget=forms.PasswordInput(attrs={'placeholder': 'Wachtwoord'}))


class UserCreateForm(forms.Form):
    error_messages = {
        "password_mismatch": "De gegeven wachtwoorden komen niet overeen.",
        "first_name_max_length": f"Voornaam is te lang. Max is {User._meta.get_field('first_name').max_length} karakters",
        "last_name_max_length": f"Achternaam is te lang. Max is {User._meta.get_field('last_name').max_length} karakters",
        "username_max_length": f"Gebruikersnaam is te lang. Max is {User._meta.get_field('username').max_length} karakters",
    }
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Wachtwoord', 'maxlength': User._meta.get_field('password').max_length}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Herhaal', 'maxlength': User._meta.get_field('password').max_length}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Gebruikersnaam', 'maxlength': User._meta.get_field('username').max_length}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Voornaam', 'maxlength': User._meta.get_field('first_name').max_length}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Achternaam', 'maxlength': User._meta.get_field('last_name').max_length}))


    def clean_first_name(self):
        if len(self.cleaned_data['first_name']) > User._meta.get_field('first_name').max_length:
            raise ValidationError(
                self.error_messages["first_name_max_length"],
                code="first_name_max_length",
            )
        return self.cleaned_data['first_name']


    def clean_last_name(self):
        if len(self.cleaned_data['last_name']) > User._meta.get_field('last_name').max_length:
            raise ValidationError(
                self.error_messages["last_name_max_length"],
                code="last_name_max_length",
            )
        return self.cleaned_data['last_name']


    def clean_username(self):
        if len(self.cleaned_data['username']) > User._meta.get_field('username').max_length:
            raise ValidationError(
                self.error_messages["username_max_length"],
                code="username_max_length",
            )
        return self.cleaned_data['username']


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self):
        user = User(username=self.cleaned_data["username"], first_name=self.cleaned_data["first_name"], last_name=self.cleaned_data["last_name"])
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user