from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    student_id = forms.CharField(label=("Student Id"),
                                 widget=forms.TextInput(attrs={'class': 'form-control'})
                                 )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(label=("Password"),
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )
    password2 = forms.CharField(label=("Password Confirmation"),
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )

    class Meta:
        model = User
        fields = ('student_id', 'email')


class LoginForm(forms.Form):
    student_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
