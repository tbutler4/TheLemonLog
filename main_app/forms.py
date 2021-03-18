from django import forms
from .models import Review, Comment
from django.contrib.auth.models import User

# class UserForm(forms.ModelForm):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField()
#     email = forms.CharField(validators=['validate_email'])
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

class EditUserForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['username', 'first_name', 'last_name']

class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter Comment'}))
    class Meta:
        model = Comment
        fields = ['comment_text']
    