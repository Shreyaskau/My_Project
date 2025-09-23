from django.urls import path
from .views import (
    UserListView, UserDetailView,
    StudentListCreateView, StudentDetailView,
    TeacherListCreateView, TeacherDetailView,
    UserRegisterView, UserLoginView,
    StudentProfileUpdateView, TeacherProfileUpdateView
)

urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
     # -------- USER ENDPOINTS --------
    path('users/', UserListView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

        # -------- STUDENT ENDPOINTS --------
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/profile/', StudentProfileUpdateView.as_view(), name='student-profile'),

    # -------- TEACHER ENDPOINTS --------
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teachers/profile/', TeacherProfileUpdateView.as_view(), name='teacher-profile'),
]