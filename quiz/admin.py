from django.contrib import admin
from .models import Quiz, Question, Option, UserQuizResult


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz_title', 'quiz_desc',
                    'created_at', 'updated_at')
    search_fields = ('quiz_title', 'quiz_desc')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question')
    search_fields = ('question',)
    list_filter = ('quiz',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option_text', 'is_correct')
    search_fields = ('option_text',)
    list_filter = ('question', 'is_correct')


@admin.register(UserQuizResult)
class UserQuizResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'score')
