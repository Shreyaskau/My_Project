from django.db import models


class Timetable(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='timetables')
    class_ref = models.ForeignKey('classes.Class', on_delete=models.CASCADE, related_name='timetables')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='timetables')
    subject = models.CharField(max_length=100)
    day_of_week = models.IntegerField()  # 0=Mon ... 6=Sun
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('school', 'class_ref', 'teacher', 'day_of_week', 'start_time')

    def __str__(self) -> str:
        return f"{self.subject} ({self.day_of_week})"

# Create your models here.
