from rest_framework import viewsets, permissions

from .models import User
from .serializers import UserSerializer


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'is_super_admin', lambda: False)())


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        return User.objects.select_related('school').all()

# Create your views here.
