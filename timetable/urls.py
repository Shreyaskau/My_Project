from rest_framework.routers import DefaultRouter

from .views import TimetableViewSet


router = DefaultRouter()
router.register(r'', TimetableViewSet, basename='timetable')

urlpatterns = router.urls





