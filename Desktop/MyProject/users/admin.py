from django.contrib import admin
from .models import User, student, teacher

# Inline for Student model inside User admin
class StudentInline(admin.StackedInline):
    model = student
    can_delete = False
    verbose_name_plural = "Student Profile"

# Inline for Teacher model inside User admin
class TeacherInline(admin.StackedInline):
    model = teacher
    can_delete = False
    verbose_name_plural = "Teacher Profile"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'role', 'is_active')
    
    # Dynamically add inline based on user's role
    def get_inlines(self, request, obj=None):
        if obj and obj.role == 'student':
            return [StudentInline]
        elif obj and obj.role == 'teacher':
            return [TeacherInline]
        return []

# Optional: register student and teacher models separately
@admin.register(student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'roll_number', 'class_name')

@admin.register(teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'subject', 'employee_id')
