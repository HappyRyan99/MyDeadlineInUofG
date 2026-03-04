from deadlinemain.forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from deadlinemain.models import Student
from deadlinemain.utils.log_utils import LogUtils

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    LogUtils.d("login_view", f"into login_view")
    if request.session.get('student_id'):
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            try:
                student = Student.objects.get(student_id=student_id)
                if check_password(password, student.auth_pwd):
                    # Login successful
                    request.session['student_id'] = str(student.student_id)  # Store as string for consistency
                    request.session['student_name'] = student.name
                    return redirect('dashboard')  # Redirect to dashboard
                else:
                    messages.error(request, "Invalid password.")
            except Student.DoesNotExist:
                messages.error(request, "Student ID not found.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    LogUtils.d("logout_view", f"User logout_view")
    try:
        del request.session['student_id']
        del request.session['student_name']
    except KeyError:
        pass
    messages.success(request, "You have been logged out.")
    return redirect('login')
