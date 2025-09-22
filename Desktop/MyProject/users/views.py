from django.shortcuts import render
from .models import User, student, teacher
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserRegisterSerializer, StudentSerializer, TeacherSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
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

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # Any authenticated user can access this view


# --------------- STUDENT VIEWS -----------------

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsTeacher | IsAdmin] # Any authenticated user can access this view

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated] # Any authenticated user can access this view

    def get_object(self):
        user = self.request.user
        if user.role == 'student':
            # Students can only see their own profile
            return user.student
        else:
            # Teachers/Admins can access any student by ID
            return student.objects.get(pk=self.kwargs['pk'])

# --------------- TEACHER VIEWS -----------------

class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin] # Only admin users can access this view

class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.role == 'teacher':
            # Teachers can only see their own profile
            return user.teacher
        else:
            # Admins can access any teacher by ID
            return teacher.objects.get(pk=self.kwargs['pk'])