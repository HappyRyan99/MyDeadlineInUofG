from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student


class RegisterForm(UserCreationForm):
    name = forms.CharField(label=("Student Name"),
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
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
        fields = ('name', 'student_id', 'email')

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        if User.objects.filter(username=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('student_id', '')
        if commit:
            user.save()
            from .models import Student
            from django.contrib.auth.hashers import make_password
            Student.objects.create(
                name=self.cleaned_data['name'],
                student_id=self.cleaned_data['student_id'],
                email=self.cleaned_data['email'],
                auth_pwd=make_password(self.cleaned_data['password1'])
            )
        return user


class LoginForm(forms.Form):
    student_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
