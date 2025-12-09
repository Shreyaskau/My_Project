from rest_framework.routers import DefaultRouter

from .views import SubscriptionPlanViewSet, SchoolSubscriptionViewSet


router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'', SchoolSubscriptionViewSet, basename='school-subscription')

urlpatterns = router.urls





