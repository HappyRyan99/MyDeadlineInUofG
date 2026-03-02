from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=50, unique=True)
    auth_pwd = models.CharField(max_length=128) # Storing hashed passwords is best practice

    def __str__(self):
        return self.name

class CourseInfo(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=50)
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE, related_name='courses', null=True)

    def __str__(self):
        return self.course_code

class GroupInfo(models.Model):
    course_code = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, related_name='groups', null=True)
    group_name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE, related_name='created_groups', null=True) # Assuming this is creator/admin

    def __str__(self):
        return self.group_name

class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='group_memberships')

    def __str__(self):
        return f"{self.student.name} in {self.group.group_name}"