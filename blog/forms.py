from django.forms import ModelForm, TextInput, Textarea, CheckboxSelectMultiple, PasswordInput, CharField

from .models import Article, User
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(ModelForm):
    """Article form"""
    class Meta:
        model = Article
        fields = ('title', 'text', 'tags')
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control'
            }),
            'text': Textarea(attrs={
                'class': 'form-control'
            }),
            'tags': CheckboxSelectMultiple()
        }


class RegistrationForm(UserCreationForm):
    """New user registration form"""
    password1 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nickname'
            })
        }
