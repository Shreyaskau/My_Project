from rest_framework import serializers

from .models import Class


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'school', 'name', 'grade', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']





