from rest_framework import viewsets, permissions

from .models import Teacher
from .serializers import TeacherSerializer


class IsPrincipalOrTeacherWithinSchool(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'school', None))


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_super_admin', lambda: False)():
            return Teacher.objects.all()
        return Teacher.objects.filter(school=user.school)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(school=user.school)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsPrincipalOrTeacherWithinSchool()]
        return super().get_permissions()

# Create your views here.
