from django import forms
from .models import Review, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators, exceptions

class UserForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", validators=[validators.UnicodeUsernameValidator, custom_validate_username])
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.', validators=[validators.validate_email])
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

def custom_validate_username(value):
    try:
        User.objects.get(username=value)
        raise exceptions.ValidationError("This username already exists, please log in with the username or choose another username.")
    except:
        return value

class EditUserForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['username', 'first_name', 'last_name', 'email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
    