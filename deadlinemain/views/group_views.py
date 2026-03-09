import json

from django.http import JsonResponse
from django.shortcuts import render, redirect

from deadlinemain.models import GroupInfo, CourseInfo, Student, GroupMember


def my_groups(request):
    # View to list student's groups
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')

def add_group(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
            group_name = data.get('group_name')
            course_id = data.get('course_id')

            if not group_name:
                return JsonResponse({'success': False, 'error': 'Group name is required'}, status=400)

            student = Student.objects.get(student_id=student_id)
            course = None
            if course_id:
                course = CourseInfo.objects.get(id=course_id, student=student)

            group = GroupInfo.objects.create(
                group_name=group_name,
                course_code=course,
                student=student
            )

            return JsonResponse({'success': True, 'group_id': group.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

def add_group_member(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')
            member_student_id = data.get('student_id')
            member_name = data.get('student_name')

            if not all([group_id, member_student_id, member_name]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

            group = GroupInfo.objects.get(id=group_id, student__student_id=student_id)

            # Create member manually
            GroupMember.objects.create(
                group=group,
                member_student_id=member_student_id,
                member_name=member_name
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
def delete_group_member(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
            member_id = data.get('member_id')

            if not member_id:
                return JsonResponse({'success': False, 'error': 'Member ID is required'}, status=400)

            # Check if member exists and if the logged-in student is the creator of the group
            member = GroupMember.objects.get(id=member_id)
            if member.group.student.student_id != student_id:
                return JsonResponse({'success': False, 'error': 'Permission denied: You are not the creator of this group'},
                                    status=403)

            member.delete()
            return JsonResponse({'success': True})
        except GroupMember.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Member not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)


def delete_group(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')

            if not group_id:
                return JsonResponse({'success': False, 'error': 'Group ID is required'}, status=400)

            group = GroupInfo.objects.get(id=group_id)
            if group.student.student_id != student_id:
                return JsonResponse({'success': False, 'error': 'Permission denied: You are not the creator of this group'},
                                    status=403)

            group.delete()
            return JsonResponse({'success': True})
        except GroupInfo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Group not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
