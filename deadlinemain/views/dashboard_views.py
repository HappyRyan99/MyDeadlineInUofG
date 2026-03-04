import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from deadlinemain.models import DeadlineTask
from deadlinemain.models import GroupInfo
from deadlinemain.models import Student
from deadlinemain.utils.log_utils import LogUtils


def index(request):
    if request.session.get('student_id'):
        return redirect('dashboard')
    else:
        return redirect('login')


def dashboard(request):
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')


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
