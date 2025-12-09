from django.db import models


class Teacher(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='teachers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('school', 'email')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Create your models here.
