from django import forms
from .models import UploadedCSVFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCSVFile
        fields = ['file']

# class QueryBuilderForm(forms.Form):
#     # Define your filter fields here
#     company_name = forms.CharField(required=False)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)    

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 