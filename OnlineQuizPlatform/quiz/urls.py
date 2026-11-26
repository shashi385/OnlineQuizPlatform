from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("profile/", views.student_profile, name="student_profile"),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="quiz/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),
    path("attempt/<int:attempt_id>/", views.take_quiz, name="take_quiz"),
    path("attempt/<int:attempt_id>/result/", views.result, name="result"),
]