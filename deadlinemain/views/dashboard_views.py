import json
from datetime import datetime
import time

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
            deadline_dt = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
            deadline = int(deadline_dt.timestamp())
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
            status='0',  # Default status
            update_time=int(time.time())
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


@require_POST
def add_task_log(request):
    LogUtils.d("add_task_log", "Received add_task_log request")
    
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        task_content = data.get('content')
        
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
            
        if not task_id or not task_content:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        if len(task_content) > 280:
            return JsonResponse({'success': False, 'error': 'Content cannot exceed 280 characters'}, status=400)
            
        task = DeadlineTask.objects.get(id=task_id)
        
        # Check permissions
        if task.student.student_id != student_id:
            # If group tasks can be updated by group members in the future, we can add logic here.
            # For now, restrict updates to the creator.
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not the creator of this task'}, status=403)
            
        from deadlinemain.models import DeadlineLog
        log = DeadlineLog.objects.create(
            task=task,
            task_content=task_content,
            create_time=int(time.time())
        )
        
        # update task's update_time
        task.update_time = int(time.time())
        task.save() 
        LogUtils.d("add_task_log", f"Log created for task {task_id}")
        
        return JsonResponse({'success': True})
        
    except DeadlineTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    except Exception as e:
        LogUtils.d("add_task_log", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def update_task_status(request):
    LogUtils.d("update_task_status", "Received update_task_status request")
    
    try:
        data = json.loads(request.body)
        task_id = data.get('id')
        status = data.get('status')
        
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
            
        if not task_id or status is None:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        task = DeadlineTask.objects.get(id=task_id)
        
        # Check permissions
        if task.student.student_id != student_id:
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not the owner of this task'}, status=403)
            
        # status could be '0' or '1'
        task.status = str(status)
        task.update_time = int(time.time()) # Update update_time
        task.save()
        
        LogUtils.d("update_task_status", f"Task {task_id} status updated to {status}")
        
        return JsonResponse({'success': True})
        
    except DeadlineTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    except Exception as e:
        LogUtils.d("update_task_status", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def edit_task(request):
    LogUtils.d("edit_task", "Received edit_task request")
    
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_title = data.get('task_title')
        new_content = data.get('content')
        
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
            
        if not task_id:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        task = DeadlineTask.objects.get(id=task_id)
        
        # Check permissions
        if task.student.student_id != student_id:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
            
        # Update fields if provided
        if new_title is not None:
            task.task_title = new_title.strip()
        if new_content is not None:
            task.content = new_content.strip()
            
        task.update_time = int(time.time())
        task.save()
        
        LogUtils.d("edit_task", f"Task {task_id} details updated")
        
        return JsonResponse({'success': True})
        
    except DeadlineTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    except Exception as e:
        LogUtils.d("edit_task", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
