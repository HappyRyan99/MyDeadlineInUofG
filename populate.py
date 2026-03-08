import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UofGdeadline.settings')
django.setup()

from deadlinemain.models import CourseInfo, GroupInfo, Student, DeadlineItem

# Create 3 new students: Sky, Cloud, Ground
from django.contrib.auth.hashers import make_password
import time
import random


def populate():
    # Ensure there is a student to assign as creator
    try:
        student = Student.objects.get(student_id='123456')
    except Student.DoesNotExist:
        print("Test student 123456 not found. Creating one.")
        student = Student.objects.create(
            name='Test Student',
            email='test@example.com',
            student_id='123456',
            auth_pwd=make_password('password')
        )

    # Populate Courses
    courses = [
        {'code': 'COMPSCI5012', 'name': 'Internet Technology 2025-26'},
        {'code': 'COMPSCI5060', 'name': 'Human Centred Security (M) 2025-26'},
        {'code': 'COMPSCI5059', 'name': 'Software Engineering (IT) - 2025-26'},
        {'code': 'ENG5044', 'name': 'Integrated Systems Design Project M (2025-26)'},
        {'code': 'COMPSCI5057', 'name': 'Human Computer Interaction Design and Evaluation (M) 2025-26'},
        {'code': 'COMPSCI5063', 'name': 'Cyber Security Fundamentals for MSc 2025-26'},
    ]

    for course_data in courses:
        course, created = CourseInfo.objects.get_or_create(
            course_code=course_data['code'],
            student=student,
            defaults={'name': course_data['name']}
        )
        if created:
            print(f"Created course: {course.course_code} - {course.name}")
        else:
            print(f"Course already exists: {course.course_code} - {course.name}")

    # Populate Groups
    groups = [
        {'code': 'COMPSCI5012', 'name': 'Group BB'},
        {'code': 'COMPSCI5060', 'name': 'Group Z'},
        {'code': 'COMPSCI5059', 'name': 'Group 37'},
        {'code': 'ENG5044', 'name': 'Group 24'},
        {'code': 'COMPSCI5057', 'name': 'Group W'},
        {'code': 'COMPSCI5063', 'name': 'LB01 Group D'},
    ]

    for group_data in groups:
        try:
            course = CourseInfo.objects.get(course_code=group_data['code'], student=student)
            group, created = GroupInfo.objects.get_or_create(
                course_code=course,
                group_name=group_data['name'],
                defaults={'student': student}
            )
            if created:
                print(f"Created group: {group.group_name} for {course.course_code}")
            else:
                print(f"Group already exists: {group.group_name} for {course.course_code}")
        except CourseInfo.DoesNotExist:
            print(f"Error: Course {group_data['code']} not found for group {group_data['name']}")

    # Populate Deadlines for student 123456
    print("Populating deadlines for student 123456...")
    try:
        student_123456 = Student.objects.get(student_id='123456')
        all_groups = list(GroupInfo.objects.filter(student=student_123456))

        current_time = int(time.time())
        day_in_seconds = 86400

        for i in range(1, 6):
            # Randomly pick a group or None
            if all_groups and random.random() > 0.2:
                group = random.choice(all_groups)
            else:
                group = None
            # Deadline between 1 and 7 days from now
            deadline_time = current_time + random.randint(1, 7) * day_in_seconds

            deadline_item, created = DeadlineItem.objects.get_or_create(
                student=student_123456,
                deadline_title=f"Deadline {i}",
                defaults={
                    'content': "Deadline content",
                    'deadline': deadline_time,
                    'status': "0",
                    'update_time': current_time,
                    'group': group
                }
            )
            if created:
                print(f"Created deadline: {deadline_item.deadline_title}")
            else:
                print(f"Deadline already exists: {deadline_item.deadline_title}")
    except Student.DoesNotExist:
        print("Student 123456 not found, skipping deadline population.")


if __name__ == '__main__':
    print("Starting population script...")
    populate()

    new_students = ['Sky', 'Cloud', 'Ground']
    test_student_id = 3070000;
    for name in new_students:
        test_student_id += 1
        email = f"{name.lower()}@gmail.com"
        password = "123456"

        try:
            student_obj, created = Student.objects.get_or_create(
                name=name,
                defaults={
                    'student_id': test_student_id,
                    'email': email,
                    'auth_pwd': make_password(password)
                }
            )
            if created:
                print(f"Created student: {name} (ID: {student_obj.student_id})")
            else:
                print(f"Student already exists: {name} (ID: {student_obj.student_id})")

            # Specific logic for Sky: Copy 3 courses from student 123456
            if name == 'Sky':
                try:
                    source_student = Student.objects.get(student_id='123456')
                    # Get first 3 courses from 123456
                    source_courses = CourseInfo.objects.filter(student=source_student)[:3]

                    for source_course in source_courses:
                        # Create copy for Sky
                        CourseInfo.objects.get_or_create(
                            course_code=source_course.course_code,  # Same course code
                            student=student_obj,
                            defaults={'name': source_course.name}
                        )
                        print(f"Assigned course {source_course.course_code} to Sky")
                except Student.DoesNotExist:
                    print("Source student 123456 not found. Cannot copy courses.")

        except Exception as e:
            print(f"Error creating student {name}: {e}")

    print("Population complete.")
