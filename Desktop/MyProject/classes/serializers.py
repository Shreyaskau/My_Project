from rest_framework import serializers
from .models import Class, Subject, TeacherAssignment, Schedule

class ClassSerializer(serializers.ModelSerializer):
    subject_names = serializers.StringRelatedField(
        source='subjects', many=True, read_only=True
    )  # for GET

    class Meta:
        model = Class
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAssignment
        fields = "__all__"
         
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"