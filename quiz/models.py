from django.db import models
from django.contrib.auth.models import User
from .utility import generate_random_id


class Quotes(models.Model):
    quote_title = models.CharField(max_length=50)
    qoute_desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    qoute_id = models.CharField(
        max_length=5, unique=True, default=generate_random_id)

    def __str__(self) -> str:
        return self.quote_title


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=50)
    quiz_desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_users = models.ManyToManyField(
        User, related_name='assigned_quiz', blank=True)
    quiz_id = models.CharField(
        max_length=5, unique=True, default=generate_random_id)

    def __str__(self):
        return self.quiz_title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class UserQuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user} - {self.quiz} - Score: {self.score}"
