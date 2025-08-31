from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView,
    LessonListCreateView, enroll_course, MyEnrollmentsView
)

urlpatterns = [
    path("courses/", CourseListCreateView.as_view(), name="course-list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list"),
    path("courses/<int:course_id>/enroll/", enroll_course, name="enroll-course"),
    path("my-enrollments/", MyEnrollmentsView.as_view(), name="my-enrollments"),
]