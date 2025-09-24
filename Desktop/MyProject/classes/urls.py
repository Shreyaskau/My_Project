from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, SubjectViewSet, TeacherAssignmentViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r'Classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'teacher-assignments', TeacherAssignmentViewSet)
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]