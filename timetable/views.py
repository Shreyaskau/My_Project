from rest_framework import viewsets, permissions

from .models import Timetable
from .serializers import TimetableSerializer


class IsPrincipalOrTeacherWithinSchool(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'school', None))


class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = TimetableSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_super_admin', lambda: False)():
            return Timetable.objects.all()
        return Timetable.objects.filter(school=user.school)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(school=user.school)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsPrincipalOrTeacherWithinSchool()]
        return super().get_permissions()

# Create your views here.
