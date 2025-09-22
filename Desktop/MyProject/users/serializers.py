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

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])  # hash the password
        user.save()
        return user