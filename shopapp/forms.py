from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.forms import MultiWidget

from .models import *


class AuthenticationForm(forms.Form):
    """ Форма авторизации """
    username = forms.CharField(max_length=100, label_suffix="", label="Логин",
                               widget=(forms.TextInput(attrs={'placeholder': 'Логин или E-mail'})))
    password = forms.CharField(widget=forms.PasswordInput, label_suffix="", label="Пароль")

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    """ Форма регистрации """
    email = forms.EmailField(
        required=True, label_suffix="", label="Email",
        error_messages={'invalid': ''}
    )
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'captcha']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldName in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldName].help_text = ''
            self.fields[fieldName].label_suffix = ''

        self.fields['username'].widget.attrs[
            'placeholder'] = 'Иванов Иван Иванович'
        self.fields['email'].widget.attrs[
            'placeholder'] = 'Пожалуйста, введите действующий email'
        self.fields['password1'].widget.attrs[
            'placeholder'] = 'Ваш пароль должен содержать как минимум 8 символов.'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2


class CustomUserProfileForm(forms.ModelForm):
    """ Форма профиля """

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'date_birth']


class CustomPasswordRestForm(PasswordResetForm):
    """ Форма сброса пароля """

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь не найден')
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    """ Форма нового пароля """
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactMessageForm(forms.ModelForm):
    """ Форма контактов """

    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']


class PostCommentsForm(forms.ModelForm):
    """ Форма комментариев """
    message = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Оставить комментарий..',
            'rows': 10,
            'cols': 100
        }))

    class Meta:
        model = PostComments
        fields = ['message']


