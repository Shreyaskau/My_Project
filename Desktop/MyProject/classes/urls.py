from django.urls import path
from .views import (
    ClassListCreateView, ClassDetailView,
    SubjectListCreateView, SubjectDetailView,
    TeacherAssignmentListCreateView, TeacherAssignmentDetailView,
    ScheduleListCreateView, ScheduleDetailView
)

urlpatterns = [
    # Classes
    path('classes/', ClassListCreateView.as_view(), name='class-list'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),

    # Subjects
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),

    # Teacher Assignments
    path('teacher-assignments/', TeacherAssignmentListCreateView.as_view(), name='teacherassignment-list'),
    path('teacher-assignments/<int:pk>/', TeacherAssignmentDetailView.as_view(), name='teacherassignment-detail'),

    # Schedules
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
]
