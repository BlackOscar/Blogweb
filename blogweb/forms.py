from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment
from crispy_forms.helper import FormHelper

class RegisterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User 
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class PostCreatedForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
    class Meta:
        model = Comment
        fields = ['comment']
