import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from deadlinemain.models import CourseInfo
from deadlinemain.models import Student
from deadlinemain.utils.log_utils import LogUtils


def course_list(request):
    # View to list all courses
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')


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
