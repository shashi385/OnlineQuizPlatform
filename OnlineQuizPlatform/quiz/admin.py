from django.contrib import admin
from .models import Quiz, Question, Attempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "duration_minutes", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "correct_option")
    list_filter = ("quiz",)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "score", "total_questions", "completed_at")
    list_filter = ("quiz",)
    readonly_fields = ("student", "quiz", "score", "total_questions", "started_at", "completed_at")
