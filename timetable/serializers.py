from rest_framework import serializers

from .models import Timetable


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = [
            'id', 'school', 'class_ref', 'teacher', 'subject', 'day_of_week',
            'start_time', 'end_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']





