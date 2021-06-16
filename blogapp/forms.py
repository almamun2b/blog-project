from .models import article, author, category, comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class crateForm(ModelForm):    
    class Meta:
        model = article
        fields = [
            'title', 'body', 'image', 'category'
            ]


class RegisterForm(UserCreationForm):
    class Meta:
        model= User
        fields = [
            'first_name', 'last_name', 'username', 'email','password1', 'password2',
        ]


class AuthorForm(ModelForm):
    class Meta:
        model= author
        fields = [
            'profile_picture', 'details'
        ]
        

class CategoryForm(ModelForm):
    class Meta:
        model = category
        fields = [
            'name'
        ]


class CommentForm(ModelForm):
    class Meta:
        model = comment
        fields = [
            'name', 'email', 'post_comment'
        ]
