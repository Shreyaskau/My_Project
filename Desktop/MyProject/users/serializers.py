from rest_framework import serializers
from .models import User, student, teacher
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']
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
    student_data = serializers.DictField(write_only=True, required=False)
    teacher_data = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'student_data', 'teacher_data']
        read_only_fields = ['id']

    def create(self, validated_data):
        student_data = validated_data.pop('student_data', {}) or {}
        teacher_data = validated_data.pop('teacher_data', {}) or {}

        # Create the user
        user = User(email=validated_data['email'], role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()

        # ---------- STUDENT CREATION ----------
        if user.role == 'student':
            defaults = {
                'name': 'Unknown',
                'age': 0,
                'number': None,  # must be unique
                'roll_number': None,
                'class_name': '',
                'admission_date': None,
                'address': '',
                'guardian_name': '',
                'guardian_contact': ''
            }
            student_data = {**defaults, **student_data}

            # Ensure unique roll_number
            if not student_data.get('roll_number'):
                unique_roll = str(uuid.uuid4())[:8]
                while student.objects.filter(roll_number=unique_roll).exists():
                    unique_roll = str(uuid.uuid4())[:8]
                student_data['roll_number'] = unique_roll
            else:
                if student.objects.filter(roll_number=student_data['roll_number']).exists():
                    raise serializers.ValidationError({
                        "roll_number": "A student with this roll number already exists."
                    })

            # Ensure unique number
            if not student_data.get('number'):
                unique_number = str(uuid.uuid4())[:8]
                while student.objects.filter(number=unique_number).exists():
                    unique_number = str(uuid.uuid4())[:8]
                student_data['number'] = unique_number
            else:
                if student.objects.filter(number=student_data['number']).exists():
                    raise serializers.ValidationError({
                        "number": "A student with this number already exists."
                    })

            student.objects.create(user=user, **student_data)

        # ---------- TEACHER CREATION ----------
        elif user.role == 'teacher':
            defaults = {
                'name': 'Unknown',
                'subject': '',
                'employee_id': str(uuid.uuid4())[:8],
                'number': str(uuid.uuid4())[:8],
                'qualification': '',
                'hire_date': None,
                'address': '',
                'salary': 0
            }
            teacher_data = {**defaults, **teacher_data}

            # Ensure unique employee_id
            if teacher.objects.filter(employee_id=teacher_data['employee_id']).exists():
                teacher_data['employee_id'] = str(uuid.uuid4())[:8]

            # Ensure unique number
            if teacher.objects.filter(number=teacher_data['number']).exists():
                teacher_data['number'] = str(uuid.uuid4())[:8]

            teacher.objects.create(user=user, **teacher_data)

        return user




class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = [
            'name', 'age', 'number', 'roll_number', 'class_name',
            'address', 'guardian_name', 'guardian_contact'
        ]

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = teacher
        fields = [
            'name', 'subject', 'employee_id', 'number',
            'qualification', 'address', 'salary'
        ]
