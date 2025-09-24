from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class Class(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, related_name="classes")
    section = models.CharField(max_length=20, blank=True, null=True)
    strength = models.PositiveIntegerField(default=0)
    description= models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}{self.section or ''}".strip()

class TeacherAssignment(models.Model):
    TEACHER_TYPE_CHOICES = [
        ('class_teacher', 'Class Teacher'),
        ('subject_teacher', 'Subject Teacher'),
    ]
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teaching_assignments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="assignments")
    teacher_type = models.CharField(max_length=20, choices = TEACHER_TYPE_CHOICES)
    qualification = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.teacher} -> {self.subject} ({self.class_obj})"
    
class Schedule(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="schedules")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_obj} - {self.subject} on {self.day} {self.start_time}-{self.end_time}"
    