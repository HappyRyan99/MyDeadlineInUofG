from django import forms
from django.contrib.auth.hashers import make_password
from .models import Student


class RegisterForm(forms.ModelForm):
    student_id = forms.CharField(label="Student Id",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="Student Name",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label="Password Confirmation",
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ('student_id', 'name', 'email')
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "The two password fields didn't match.")

        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        student.auth_pwd = make_password(self.cleaned_data["password"])
        if commit:
            student.save()
        return student


class LoginForm(forms.Form):
    student_id = forms.CharField(
        label="Student Id",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
