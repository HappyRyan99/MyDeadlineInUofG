import time
from datetime import datetime

from django.http import JsonResponse

from deadlinemain.models import CourseInfo
from deadlinemain.models import Student, DeadlineItem, GroupInfo
from deadlinemain.utils.log_utils import LogUtils

day_second = 86400
time_format_HM = '%Y-%m-%d %H:%M'
time_format_HMS = '%Y-%m-%d %H:%M:%S'


def dashboard_meta(request):
    """
    Returns student info and groups. Very fast.
    """
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    try:
        student = Student.objects.get(student_id=student_id)
        student_data = {
            'name': student.name,
            'student_id': student.student_id,
            'email': student.email
        }

        # Groups Info
        created_groups = GroupInfo.objects.filter(student=student)
        member_groups_std = GroupInfo.objects.filter(members__student=student)
        member_groups_id = GroupInfo.objects.filter(members__member_student_id=student.student_id)
        user_groups = (created_groups | member_groups_std | member_groups_id).distinct().select_related('course_code')

        groups_data = [{
            'id': group.id,
            'group_name': group.group_name,
            'course_code': group.course_code.course_code if group.course_code else '',
            'course_name': group.course_code.name if group.course_code else ''
        } for group in user_groups]

        return JsonResponse({
            'success': True,
            'data': {
                'student': student_data,
                'groups': groups_data
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        LogUtils.d("dashboard_meta", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def dashboard_deadlines(request):
    """
    Returns deadlines and stats. Optimized with eager loading.
    """
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    try:
        student = Student.objects.get(student_id=student_id)
        
        # Get groups first for filtering shared deadlines
        created_groups = GroupInfo.objects.filter(student=student)
        member_groups_std = GroupInfo.objects.filter(members__student=student)
        member_groups_id = GroupInfo.objects.filter(members__member_student_id=student.student_id)
        user_groups = (created_groups | member_groups_std | member_groups_id).distinct()

        # Eager load groups and logs to avoid N+1 queries
        personal_deadlines = DeadlineItem.objects.filter(student=student)
        shared_deadlines = DeadlineItem.objects.filter(group__in=user_groups)
        
        deadlines = (personal_deadlines | shared_deadlines).distinct().order_by('deadline')\
            .select_related('group', 'group__course_code')\
            .prefetch_related('logs')

        now_int = int(time.time())
        one_day_limit = now_int + day_second
        three_day_limit = now_int + 3 * day_second
        seven_day_limit = now_int + 7 * day_second

        deadlines_data = []
        stats = {
            'deadlines_1_day': [],
            'deadlines_3_day': [],
            'deadlines_7_day': [],
        }

        for t in deadlines:
            delta_seconds = t.deadline - now_int
            hours_until = delta_seconds / 3600.0
            
            # Prefetched logs - sorted in memory to avoid extra query
            logs_list = sorted(list(t.logs.all()), key=lambda x: x.create_time, reverse=True)
            logs_data = [{
                'id': log.id,
                'content': log.deadline_content,
                'create_time': datetime.fromtimestamp(log.create_time).strftime(time_format_HMS)
            } for log in logs_list]

            deadline_formatted = datetime.fromtimestamp(t.deadline).strftime(time_format_HM)
            
            # Build basic data
            item = {
                'id': t.id,
                'deadline_title': t.deadline_title,
                'content': t.content,
                'deadline': deadline_formatted,
                'is_past_due': delta_seconds < 0,
                'hours_until': hours_until,
                'days_until': int(delta_seconds / day_second),
                'status': t.status,
                'update_time': datetime.fromtimestamp(t.update_time).isoformat() + 'Z' if t.update_time else None,
                'update_time_display': datetime.fromtimestamp(t.update_time).strftime(time_format_HM) if t.update_time else None,
                'logs': logs_data,
                'can_edit': True,
                'is_creator': t.student_id == student.student_id,
                'group': {
                    'group_name': t.group.group_name,
                    'course_name': t.group.course_code.name if t.group.course_code else '',
                    'course_code': t.group.course_code.course_code if t.group.course_code else ''
                } if t.group else None
            }
            deadlines_data.append(item)

            # Categorize for stats (only if active)
            if t.status == '0' and delta_seconds >= 0:
                if t.deadline <= one_day_limit:
                    stats['deadlines_1_day'].append(t.deadline_title)
                if t.deadline <= three_day_limit:
                    stats['deadlines_3_day'].append(t.deadline_title)
                if t.deadline <= seven_day_limit:
                    stats['deadlines_7_day'].append(t.deadline_title)

        return JsonResponse({
            'success': True,
            'data': {
                'deadlines': deadlines_data,
                'stats': stats
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        LogUtils.d("dashboard_deadlines", f"Error: {str(e)}")
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
        # Groups where the student is a creator OR a member
        created_groups = GroupInfo.objects.filter(student=student)
        member_groups_std = GroupInfo.objects.filter(members__student=student)
        member_groups_id = GroupInfo.objects.filter(members__member_student_id=student.student_id)

        groups = (created_groups | member_groups_std | member_groups_id).distinct()

        groups_data = []
        for group in groups:
            members = []
            for m in group.members.all():
                if m.student:
                    members.append({
                        'id': m.id,
                        'name': m.student.name,
                        'student_id': m.student.student_id,
                        'is_manual': False
                    })
                else:
                    members.append({
                        'id': m.id,
                        'name': m.member_name,
                        'student_id': m.member_student_id,
                        'is_manual': True
                    })

            groups_data.append({
                'id': group.id,
                'group_name': group.group_name,
                'course_code': group.course_code.course_code if group.course_code else '',
                'course_name': group.course_code.name if group.course_code else '',
                'creator_name': group.student.name if group.student else 'Unknown',
                'is_creator': group.student == student,
                'members': members
            })

        # Fetch courses for dropdown
        courses = CourseInfo.objects.filter(student=student)
        courses_data = [{
            'id': c.id,
            'course_code': c.course_code,
            'name': c.name
        } for c in courses]

        return JsonResponse({
            'success': True,
            'data': {
                'student': {
                    'name': student.name,
                    'student_id': student.student_id
                },
                'groups': groups_data,
                'courses': courses_data
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        LogUtils.d("my_groups_data", f"Error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
