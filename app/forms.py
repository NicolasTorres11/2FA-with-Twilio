from django.forms import ModelForm, CharField, PasswordInput
from app.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(ModelForm):
    password = CharField(widget=PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'phone_number']