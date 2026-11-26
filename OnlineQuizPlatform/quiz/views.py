from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import RegisterForm
from .models import Quiz, Question, Attempt


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "quiz/register.html", {"form": form})


@login_required
def dashboard(request):
    quizzes = Quiz.objects.filter(is_active=True).prefetch_related("questions")
    attempts = Attempt.objects.filter(student=request.user, completed_at__isnull=False)[:8]
    return render(request, "quiz/dashboard.html", {"quizzes": quizzes, "attempts": attempts})


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    return render(request, "quiz/quiz_detail.html", {"quiz": quiz})


@login_required
@require_POST
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    if not quiz.questions.exists():
        messages.error(request, "This quiz does not have any questions yet.")
        return redirect("dashboard")
    attempt = Attempt.objects.create(
        student=request.user,
        quiz=quiz,
        total_questions=quiz.questions.count(),
    )
    request.session[f"attempt_{attempt.id}_started"] = timezone.now().isoformat()
    return redirect("take_quiz", attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, student=request.user)
    if attempt.completed_at:
        return redirect("result", attempt_id=attempt.id)

    questions = list(attempt.quiz.questions.all())
    start_string = request.session.get(f"attempt_{attempt.id}_started")
    if not start_string:
        # A missing session start marker should not grant extra time.
        started = attempt.started_at
    else:
        from django.utils.dateparse import parse_datetime
        started = parse_datetime(start_string) or attempt.started_at

    deadline = started + timedelta(minutes=attempt.quiz.duration_minutes)
    remaining_seconds = max(0, int((deadline - timezone.now()).total_seconds()))

    if request.method == "POST":
        score = 0
        # Enforce the deadline on the server as well as showing a browser timer.
        if timezone.now() <= deadline:
            for question in questions:
                selected = request.POST.get(f"question_{question.id}", "")
                if selected == question.correct_option:
                    score += 1
        attempt.score = score
        attempt.total_questions = len(questions)
        attempt.completed_at = timezone.now()
        attempt.save()
        request.session.pop(f"attempt_{attempt.id}_started", None)
        return redirect("result", attempt_id=attempt.id)

    if remaining_seconds <= 0:
        attempt.score = 0
        attempt.total_questions = len(questions)
        attempt.completed_at = timezone.now()
        attempt.save()
        return redirect("result", attempt_id=attempt.id)

    return render(request, "quiz/take_quiz.html", {
        "attempt": attempt,
        "questions": questions,
        "remaining_seconds": remaining_seconds,
    })


@login_required
def result(request, attempt_id):
    attempt = get_object_or_404(
        Attempt, id=attempt_id, student=request.user, completed_at__isnull=False
    )
    return render(request, "quiz/result.html", {"attempt": attempt})
@login_required
def student_profile(request):
    attempts = Attempt.objects.filter(
        student=request.user,
        completed_at__isnull=False
    ).select_related("quiz")

    attempts_list = list(attempts)

    total_attempts = len(attempts_list)

    if total_attempts > 0:
        highest_percentage = max(
            attempt.percentage for attempt in attempts_list
        )

        average_percentage = round(
            sum(attempt.percentage for attempt in attempts_list)
            / total_attempts,
            2
        )
    else:
        highest_percentage = 0
        average_percentage = 0

    context = {
        "attempts": attempts_list,
        "total_attempts": total_attempts,
        "highest_percentage": highest_percentage,
        "average_percentage": average_percentage,
    }
    

    return render(request, "quiz/profile.html", context)
