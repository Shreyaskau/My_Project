from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        PRINCIPAL = 'principal', 'Principal'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    role = models.CharField(max_length=32, choices=Roles.choices, default=Roles.STUDENT)
    school = models.ForeignKey('schools.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def is_super_admin(self) -> bool:
        return self.role == self.Roles.SUPER_ADMIN

    def is_principal(self) -> bool:
        return self.role == self.Roles.PRINCIPAL

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

# Create your models here.
