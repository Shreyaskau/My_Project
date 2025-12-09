from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'is_super_admin', lambda: False)())


class IsPrincipal(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'is_principal', lambda: False)())


class IsInSameSchool(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        obj_school = getattr(obj, 'school', None)
        return bool(user and user.is_authenticated and obj_school and user.school_id == getattr(obj_school, 'id', None))


