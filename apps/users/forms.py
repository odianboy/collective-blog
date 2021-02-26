from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from apps.users.models import AuthorProfile


class CustomCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = AuthorProfile
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):
    phone = forms.CharField(required=False)
    skype = forms.CharField(required=False)
    password = None  # TODO: check

    class Meta(UserChangeForm.Meta):
        model = AuthorProfile
        fields = ('first_name', 'last_name', 'avatar', 'phone', 'skype')


class LoginForm(AuthenticationForm):
    email = forms.CharField(label='Email')
