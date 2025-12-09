from django.db import models


class Student(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    enrollment_number = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('school', 'enrollment_number')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Create your models here.
