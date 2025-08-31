from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer
from rest_framework.exceptions import PermissionDenied

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by("-created_at")
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Only teachers can create courses
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can create courses.")
        serializer.save(teacher=self.request.user)

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Teacher must own the course
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)
        if course.teacher != self.request.user:
            raise PermissionDenied("You may only add lessons to your own course.")
        serializer.save()

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher == request.user:
        return Response({"detail": "Teacher cannot enroll as learner"}, status=status.HTTP_400_BAD_REQUEST)
    obj, created = Enrollment.objects.get_or_create(course=course, learner=request.user)
    serializer = EnrollmentSerializer(obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(learner=self.request.user).select_related("course")