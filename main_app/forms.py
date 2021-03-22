from django import forms
from .models import Review, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core import exceptions
from django.contrib.auth.validators import UnicodeUsernameValidator


def custom_validate_username(value):
    try:
        User.objects.get(username=value)
        raise exceptions.ValidationError("This username already exists, please log in with the username or choose another username.")
    except:
        return value


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", validators=[UnicodeUsernameValidator, custom_validate_username])
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.', validators=[validate_email])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')

class EditUserForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['username', 'first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Enter Comment', 'maxlength':'240'}))
    class Meta:
        model = Comment
        fields = ['comment_text']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','description', 'product', 'rating']