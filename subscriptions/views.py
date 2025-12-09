from rest_framework import viewsets, permissions

from .models import SubscriptionPlan, SchoolSubscription
from .serializers import SubscriptionPlanSerializer, SchoolSubscriptionSerializer


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'is_super_admin', lambda: False)())


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all().order_by('price_cents')
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsSuperAdmin]


class SchoolSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_super_admin', lambda: False)():
            return SchoolSubscription.objects.all()
        # Principals limited to their own
        return SchoolSubscription.objects.filter(school=user.school)

    def perform_create(self, serializer):
        user = self.request.user
        if getattr(user, 'is_super_admin', lambda: False)():
            serializer.save()
        else:
            serializer.save(school=user.school)

# Create your views here.
