from django.shortcuts import render
from .models import User, student, teacher
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserRegisterSerializer, StudentSerializer, TeacherSerializer, StudentProfileSerializer, TeacherProfileSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': "Provide email and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'role': user.role, 'email': user.email}, status=status.HTTP_200_OK)

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin] # Only admin users can access this view
    authentication_classes = [TokenAuthentication]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # Any authenticated user can access this view
    

# --------------- STUDENT VIEWS -----------------

class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsTeacher | IsAdmin]  # only teachers or admins
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # Admin sees all students
            return student.objects.all()
        elif user.role == 'teacher':
            # Teachers can see all students (remove teacher_classes filter if not ready)
            return student.objects.all()
        else:
            # Other users shouldn't see the list
            return student.objects.none()

    def perform_create(self, serializer):
        # Only admins can create students; adjust as needed
        if self.request.user.role in ['admin', 'teacher']:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You do not have permission to create students.")

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        user = self.request.user
        if user.role == 'student':
            return user.student
        else:
            return student.objects.get(pk=self.kwargs['pk'])

class StudentProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        user = self.request.user
        if user.role != 'student':
            raise PermissionDenied("Only students can access this endpoint")

        # fetch existing profile
        student_profile = getattr(user, 'student', None)
        if not student_profile:
            raise NotFound("Student profile does not exist. Contact admin to create one.")
        return student_profile

# --------------- TEACHER VIEWS -----------------

class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin] # Only admin users can access this view
    authentication_classes = [TokenAuthentication]

class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        user = self.request.user
        if user.role == "teacher":
            return user.teacher   # only their own profile
        elif user.role == "admin":
            return teacher.objects.get(pk=self.kwargs['pk'])
        else:
            raise PermissionDenied("You do not have access to this resource.")

class TeacherProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        user = self.request.user
        if user.role != 'teacher':
            raise PermissionDenied("Only teachers can access this endpoint")

        teacher_profile = getattr(user, 'teacher', None)
        if not teacher_profile:
            raise NotFound("Teacher profile does not exist. Contact admin to create one.")
        return teacher_profile