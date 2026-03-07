import time
from datetime import datetime

from django.http import JsonResponse

from deadlinemain.models import CourseInfo
from deadlinemain.models import Student, DeadlineTask, GroupInfo
from deadlinemain.utils.log_utils import LogUtils

day_second = 86400
time_format_HM = '%Y-%m-%d %H:%M'
time_format_HMS = '%Y-%m-%d %H:%M:%S'
def dashboard_data(request):
    LogUtils.d("dashboard_data", f"enter this")
    """
    Returns the data needed to render the Vue Dashboard.
    Requires an active session for a student.
    """
    student_id = request.session.get('student_id')

    if not student_id:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    try:
        student = Student.objects.get(student_id=student_id)

        # Student Info
        student_data = {
            'name': student.name,
            'student_id': student.student_id,
            'email': student.email
        }

        # Groups Info (where student created it or associated with it depending on current logic)
        user_groups = GroupInfo.objects.filter(student__student_id=student.student_id)
        groups_data = [{
            'id': group.id,
            'group_name': group.group_name,
            'course_code': group.course_code.course_code if group.course_code else '',
            'course_name': group.course_code.name if group.course_code else ''
        } for group in user_groups]

        # Tasks Info
        now_int = int(time.time())
        tasks = DeadlineTask.objects.filter(student=student).order_by('deadline')

        one_day_limit_str = datetime.fromtimestamp(now_int + day_second).strftime(time_format_HM)
        three_day_limit_str = datetime.fromtimestamp(now_int + 3 * day_second).strftime(time_format_HM)
        seven_day_limit_str = datetime.fromtimestamp(now_int + 7 * day_second).strftime(time_format_HM)
        now_str = datetime.fromtimestamp(now_int).strftime(time_format_HM)

        tasks_data = []
        for t in tasks:
            # Calculate precise hours difference
            delta_seconds = t.deadline - now_int
            hours_until = delta_seconds / 3600.0
            logs_data = [{
                'id': log.id,
                'content': log.task_content,
                'create_time': datetime.fromtimestamp(log.create_time).strftime(time_format_HMS)
            } for log in t.logs.all().order_by('-create_time')]
            
            tasks_data.append({
                'id': t.id,
                'task_title': t.task_title,
                'content': t.content,
                'deadline': datetime.fromtimestamp(t.deadline).strftime(time_format_HM),
                'is_past_due': delta_seconds < 0,
                'hours_until': hours_until,
                'days_until': int(delta_seconds / day_second),
                'status': t.status,
                'update_time': datetime.fromtimestamp(t.update_time).isoformat() + 'Z' if t.update_time else None,
                'update_time_display': datetime.fromtimestamp(t.update_time).strftime(time_format_HM) if t.update_time else None,
                'logs': logs_data,
                'group': {
                    'group_name': t.group.group_name,
                    'course_name': t.group.course_code.name if t.group.course_code else '',
                    'course_code': t.group.course_code.course_code if t.group.course_code else ''
                } if t.group else None
            })

        # Limits and categorized for stats
        stats = {
            'tasks_1_day': [t['task_title'] for t in tasks_data if
                            t['deadline'] <= one_day_limit_str and t['deadline'] >= now_str],
            'tasks_3_day': [t['task_title'] for t in tasks_data if
                            t['deadline'] <= three_day_limit_str and t['deadline'] >= now_str],
            'tasks_7_day': [t['task_title'] for t in tasks_data if
                            t['deadline'] <= seven_day_limit_str and t['deadline'] >= now_str],
        }

        return JsonResponse({
            'success': True,
            'data': {
                'student': student_data,
                'groups': groups_data,
                'tasks': tasks_data,
                'stats': stats
            }
        })

    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        LogUtils.d("dashboard_data", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def course_list_data(request):
    """
    Returns the data needed to render the Vue Courses view.
    Requires an active session for a student.
    """
    student_id = request.session.get('student_id')

    if not student_id:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    try:
        student = Student.objects.get(student_id=student_id)
        courses = CourseInfo.objects.filter(student__student_id=student.student_id)

        courses_data = [{
            'id': course.id,
            'course_code': course.course_code,
            'name': course.name
        } for course in courses]

        return JsonResponse({
            'success': True,
            'data': {
                'student': {
                    'name': student.name,
                    'student_id': student.student_id
                },
                'courses': courses_data
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        LogUtils.d("course_list_data", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def my_groups_data(request):
    """
    Returns the data needed to render the Vue Groups view.
    Requires an active session for a student.
    """
    student_id = request.session.get('student_id')

    if not student_id:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    try:
        student = Student.objects.get(student_id=student_id)
        groups = GroupInfo.objects.filter(student__student_id=student.student_id)

        groups_data = []
        for group in groups:
            members = [{'name': m.student.name} for m in group.members.all()]
            groups_data.append({
                'id': group.id,
                'group_name': group.group_name,
                'course_code': group.course_code.course_code if group.course_code else '',
                'course_name': group.course_code.name if group.course_code else '',
                'creator_name': group.student.name if group.student else 'Unknown',
                'members': members
            })

        return JsonResponse({
            'success': True,
            'data': {
                'student': {
                    'name': student.name,
                    'student_id': student.student_id
                },
                'groups': groups_data
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        LogUtils.d("my_groups_data", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
