from rest_framework import serializers
from .models import Course, Lesson, Enrollment
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "course", "title", "content", "order")

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "title", "description", "teacher", "created_at", "lessons")

class EnrollmentSerializer(serializers.ModelSerializer):
    learner = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ("id", "learner", "course", "enrolled_at")