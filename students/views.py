from rest_framework import viewsets, permissions

from .models import Student
from .serializers import StudentSerializer


class IsPrincipalOrTeacherWithinSchool(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'school', None))


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_super_admin', lambda: False)():
            return Student.objects.all()
        return Student.objects.filter(school=user.school)

    def perform_create(self, serializer):
        user = self.request.user
        school = user.school
        serializer.save(school=school)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsPrincipalOrTeacherWithinSchool()]
        return super().get_permissions()

# Create your views here.
