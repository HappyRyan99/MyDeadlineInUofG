import json
from datetime import datetime
import time

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from deadlinemain.models import DeadlineItem
from deadlinemain.models import GroupInfo
from deadlinemain.models import Student
from deadlinemain.models import DeadlineLog
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
def add_deadline(request):
    LogUtils.d("add_deadline", "Received add_deadline request")

    try:
        data = json.loads(request.body)
        deadline_title = data.get('deadline_title')
        content = data.get('content')
        deadline_str = data.get('deadline')  # yyyy-mm-dd HH:mm
        group_id = data.get('group_id')

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        student = Student.objects.get(student_id=student_id)

        # Validate required fields
        if not deadline_title or not content or not deadline_str:
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
                # Optional: Check if student is allowed to add deadline to this group
            except GroupInfo.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Group not found'}, status=404)

        # Create Deadline
        deadline_item = DeadlineItem.objects.create(
            student=student,
            group=group,
            deadline_title=deadline_title,
            content=content,
            deadline=deadline,
            status='0',  # Default status
            update_time=int(time.time())
        )

        LogUtils.d("add_deadline", f"Deadline created: {deadline_item.deadline_title} (ID: {deadline_item.id})")

        return JsonResponse({'success': True})

    except Exception as e:
        LogUtils.d("add_deadline", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def delete_deadline(request):
    LogUtils.d("delete_deadline", "Received delete_deadline request")

    try:
        data = json.loads(request.body)
        deadline_id = data.get('id')

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)

        if not deadline_id:
            return JsonResponse({'success': False, 'error': 'Deadline ID required'}, status=400)

        # Verify deadline exists and belongs to student
        deadline_item = DeadlineItem.objects.get(id=deadline_id)

        # Check ownership
        if deadline_item.student.student_id != student_id:
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not the creator of this deadline'},
                                status=403)

        deadline_item.delete()
        LogUtils.d("delete_deadline", f"Deadline {deadline_id} deleted by {student_id}")

        return JsonResponse({'success': True})

    except DeadlineItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Deadline not found'}, status=404)
    except Exception as e:
        LogUtils.d("delete_deadline", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def add_deadline_log(request):
    LogUtils.d("add_deadline_log", "Received add_deadline_log request")
    
    try:
        data = json.loads(request.body)
        deadline_id = data.get('deadline_id')
        deadline_content = data.get('content')
        
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
            
        if not deadline_id or not deadline_content:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        if len(deadline_content) > 280:
            return JsonResponse({'success': False, 'error': 'Content cannot exceed 280 characters'}, status=400)
            
        deadline_item = DeadlineItem.objects.get(id=deadline_id)
        
        # Check permissions
        if deadline_item.student.student_id != student_id:
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not the creator of this deadline'}, status=403)
            
        log = DeadlineLog.objects.create(
            deadline=deadline_item,
            deadline_content=deadline_content,
            create_time=int(time.time())
        )
        
        # update deadline's update_time
        deadline_item.update_time = int(time.time())
        deadline_item.save() 
        LogUtils.d("add_deadline_log", f"Log created for deadline {deadline_id}")
        
        return JsonResponse({'success': True})
        
    except DeadlineItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Deadline not found'}, status=404)
    except Exception as e:
        LogUtils.d("add_deadline_log", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def update_deadline_status(request):
    LogUtils.d("update_deadline_status", "Received update_deadline_status request")
    
    try:
        data = json.loads(request.body)
        deadline_id = data.get('id')
        status = data.get('status')
        
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
            
        if not deadline_id or status is None:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        deadline_item = DeadlineItem.objects.get(id=deadline_id)
        
        # Check permissions
        if deadline_item.student.student_id != student_id:
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not the owner of this deadline'}, status=403)
            
        # status could be '0' or '1'
        deadline_item.status = str(status)
        deadline_item.update_time = int(time.time()) # Update update_time
        deadline_item.save()
        
        LogUtils.d("update_deadline_status", f"Deadline {deadline_id} status updated to {status}")
        
        return JsonResponse({'success': True})
        
    except DeadlineItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Deadline not found'}, status=404)
    except Exception as e:
        LogUtils.d("update_deadline_status", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def edit_deadline(request):
    LogUtils.d("edit_deadline", "Received edit_deadline request")
    
    try:
        data = json.loads(request.body)
        deadline_id = data.get('deadline_id')
        new_title = data.get('deadline_title')
        new_content = data.get('content')
        
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=403)
            
        if not deadline_id:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        deadline_item = DeadlineItem.objects.get(id=deadline_id)
        
        # Check permissions: Creator OR Member of the associated group
        is_creator = deadline_item.student.student_id == student_id
        is_member = False
        if deadline_item.group:
            is_reg_member = deadline_item.group.members.filter(student__student_id=student_id).exists()
            is_manual_member = deadline_item.group.members.filter(member_student_id=student_id).exists()
            is_member = is_reg_member or is_manual_member
            
        if not (is_creator or is_member):
            return JsonResponse({'success': False, 'error': 'Permission denied: You are not authorized to edit this deadline'}, status=403)
            
        # Update fields if provided
        if new_title is not None:
            deadline_item.deadline_title = new_title.strip()
        if new_content is not None:
            deadline_item.content = new_content.strip()
            
        deadline_item.update_time = int(time.time())
        deadline_item.save()
        
        LogUtils.d("edit_deadline", f"Deadline {deadline_id} details updated")
        
        return JsonResponse({'success': True})
        
    except DeadlineItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Deadline not found'}, status=404)
    except Exception as e:
        LogUtils.d("edit_deadline", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
