from django.contrib import admin
from .models import Quiz, Question, Option, UserQuizResult, Quotes


@admin.register(Quotes)
class QouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'quote_title', 'qoute_desc',
                    'created_by', 'qoute_id')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz_title', 'quiz_desc',
                    'quiz_id')


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
