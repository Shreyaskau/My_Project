from rest_framework import serializers
from .models import User, student, teacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested User Info

    class Meta:
        model = student
        fields = [
            'id', 'user', 'name' ,'age', 'number', 'roll_number', 'class_name', 
            'admission_date', 'address', 'guardian_name', 'guardian_contact'
        ]
        read_only_fields = ['id', 'admission_date']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested User Info

    class Meta:
        model = teacher
        fields = [
            'id', 'user', 'name', 'subject', 'employee_id', 'number', 
            'qualification', 'hire_date', 'address', 'salary'
        ]
        read_only_fields = ['id','hire_date']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Optional: allow profile fields during registration
    student_data = serializers.DictField(write_only=True, required=False)
    teacher_data = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'student_data', 'teacher_data']
        read_only_fields = ['id']

    def create(self, validated_data):
        student_data = validated_data.pop('student_data', None)
        teacher_data = validated_data.pop('teacher_data', None)

        user = User(
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Auto-create profile
        if user.role == 'student':
            student.objects.create(user=user, **(student_data or {}))
        elif user.role == 'teacher':
            teacher.objects.create(user=user, **(teacher_data or {}))

        return user
