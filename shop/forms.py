import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=13,
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(attrs={
            'placeholder': '+375XXXXXXXXX',
            'pattern': r'^\+?\d{1,12}$',
            'title': 'Введите телефон в формате +375XXXXXXXXX (только цифры и знак +, максимум 13 символов)'
        })
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
            "password1": "Пароль",
            "password2": "Повторите пароль",
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.fullmatch(r'\+?\d{1,12}', phone):
            raise forms.ValidationError(
                "Телефон должен содержать только цифры и необязательный +, максимум 13 символов"
            )
        return phone