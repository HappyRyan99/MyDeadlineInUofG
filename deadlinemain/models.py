from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=50, unique=True)
    auth_pwd = models.CharField(max_length=128)  # Storing hashed passwords is best practice

    def __str__(self):
        return self.name


class CourseInfo(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=50)
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE, related_name='courses',
                                null=True)

    def __str__(self):
        return self.course_code


class GroupInfo(models.Model):
    course_code = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, related_name='groups', null=True)
    group_name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE, related_name='created_groups',
                                null=True)  # Assuming this is creator/admin

    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    id = models.CharField(primary_key=True, default=models, editable=False)
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='group_memberships')

    def __str__(self):
        return f"{self.student.name} in {self.group.group_name}"


class DeadlineTask(models.Model):
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE, related_name='created_tasks')
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    task_title = models.CharField(max_length=200)
    content = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50)  # Could use choices
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title


class DeadlineLog(models.Model):
    task = models.ForeignKey(DeadlineTask, on_delete=models.CASCADE, related_name='logs')
    task_content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.task.task_title}"
