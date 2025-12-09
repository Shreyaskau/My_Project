from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ------------------ Custom Manager ------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# ------------------ User Model ------------------
class User(AbstractUser):
    username = None
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher','Teacher'),
        ('student','Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no other required fields

    objects = CustomUserManager()  # attach custom manager

    def __str__(self):
        return f"{self.email} ({self.role})"

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    number = models.CharField(max_length=15, unique=True)
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    class_name = models.CharField(max_length=50)
    admission_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True, null= True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=15, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.roll_number} - {self.name}"
    
class teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.subject})"