from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import Student


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
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

def course_list(request):
    # View to list all courses
    from .models import CourseInfo
    student_id = request.session.get('student_id')
    student = None
    if student_id:
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            pass

    if student:
        courses = CourseInfo.objects.filter(student__student_id=student.student_id)
    else:
        courses = []

    return render(request, 'deadlinemain/course_list.html', {'courses': courses, 'student': student})


def my_groups(request):
    # View to list student's groups
    from .models import GroupInfo
    student_id = request.session.get('student_id')
    student = None
    groups = []

    if student_id:
        try:
            student = Student.objects.get(student_id=student_id)
            # Fetch groups where the student is the creator (based on previous task)
            groups = GroupInfo.objects.filter(student__student_id=student.student_id)
        except Student.DoesNotExist:
            pass

    return render(request, 'deadlinemain/my_groups.html', {'groups': groups, 'student': student})


# from django.contrib.auth.decorators import login_required # Not used for custom session auth

# @login_required # Causes redirect to /accounts/login/ for custom session auth
@require_POST
def add_course(request):
    try:
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': f'Student not found {student_id}'}, status=403)


@require_POST
def delete_course(request):
    import json
    from .models import CourseInfo
    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        # Verify student owns the course
        course = CourseInfo.objects.get(id=course_id, student__student_id=student_id)

        # Check for existing groups
        if course.groups.exists():
            return JsonResponse({'success': False,
                                 'error': 'Cannot delete course with existing groups. Please delete the groups first.'},
                                status=400)

        course.delete()
        return JsonResponse({'success': True})

    except CourseInfo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found or access denied'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def edit_course(request):
    import json
    from .models import CourseInfo
    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')
        new_name = data.get('name')

        if not new_name:
            return JsonResponse({'success': False, 'error': 'Course name cannot be empty'}, status=400)

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        # Verify student owns the course
        course = CourseInfo.objects.get(id=course_id, student__student_id=student_id)

        course.name = new_name
        course.save()
        return JsonResponse({'success': True})

    except CourseInfo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found or access denied'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
        from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'login.html')
