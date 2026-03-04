import json
from datetime import datetime

from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import CourseInfo
from .models import DeadlineTask
from .models import GroupInfo
from .models import Student
from .utils.log_utils import LogUtils

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


def index(request):
    if request.session.get('student_id'):
        return redirect('dashboard')
    else:
        form = LoginForm()

    return redirect(login_view)


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


def dashboard(request):
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')


def logout_view(request):
    LogUtils.d("logout_view", f"User logout_view")
    try:
        del request.session['student_id']
        del request.session['student_name']
    except KeyError:
        pass
    messages.success(request, "You have been logged out.")
    return redirect('login')


def course_list(request):
    # View to list all courses
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')


def my_groups(request):
    # View to list student's groups
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')

# @login_required # Causes redirect to /accounts/login/ for custom session auth

@require_POST
def add_course(request):
    try:
        data = json.loads(request.body)
        course_code = data.get('course_code')
        name = data.get('name')

        if not course_code or not name:
            return JsonResponse({'success': False, 'error': 'Course code and name are required'}, status=400)

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        student = Student.objects.get(student_id=student_id)

        # Check if course with this code already exists for student
        if CourseInfo.objects.filter(student=student, course_code=course_code).exists():
            return JsonResponse({'success': False, 'error': 'Course with this code already exists'}, status=400)

        CourseInfo.objects.create(
            name=name,
            course_code=course_code,
            student=student
        )
        return JsonResponse({'success': True})

    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': f'Student not found'}, status=403)
    except Exception as e:
        LogUtils.d("add_course", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@require_POST
def delete_course(request):
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



@require_POST
def add_task(request):
    LogUtils.d("add_task", "Received add_task request")

    try:
        data = json.loads(request.body)
        task_title = data.get('task_title')
        content = data.get('content')
        deadline_str = data.get('deadline')  # yyyy-mm-dd HH:mm
        group_id = data.get('group_id')

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        student = Student.objects.get(student_id=student_id)

        # Validate required fields
        if not task_title or not content or not deadline_str:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

        # Parse deadline
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format. Expected yyyy-mm-dd HH:mm'},
                                status=400)

        group = None
        if group_id:
            try:
                group = GroupInfo.objects.get(id=group_id)
                # Optional: Check if student is allowed to add task to this group
            except GroupInfo.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Group not found'}, status=404)

        # Create Task
        task = DeadlineTask.objects.create(
            student=student,
            group=group,
            task_title=task_title,
            content=content,
            deadline=deadline,
            status='0'  # Default status
        )

        LogUtils.d("add_task", f"Task created: {task.task_title} (ID: {task.id})")

        return JsonResponse({'success': True})

    except Exception as e:
        LogUtils.d("add_task", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@require_POST
def delete_task(request):
    LogUtils.d("delete_task", "Received delete_task request")

    try:
        data = json.loads(request.body)
        task_id = data.get('id')

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        if not task_id:
            return JsonResponse({'success': False, 'error': 'Task ID required'}, status=400)

        # Verify task exists and belongs to student
        task = DeadlineTask.objects.get(id=task_id)

        # Check ownership
        # Note: task.student is the Student object, task.student.student_id is the string ID
        if task.student.student_id != student_id:
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not the creator of this task'},
                                status=403)

        task.delete()
        LogUtils.d("delete_task", f"Task {task_id} deleted by {student_id}")

        return JsonResponse({'success': True})

    except DeadlineTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    except Exception as e:
        LogUtils.d("delete_task", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def custom_page_not_found(request, exception):
    # Differentiate missing paths by HTTP method
    if request.method == 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested endpoint does not exist.',
        }, status=404)

    # For GET requests, serve the custom 404 HTML page
    return render(request, '404.html', status=404)