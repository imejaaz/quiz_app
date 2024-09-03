from django.db import models
from django.contrib.auth.models import User
from .utility import generate_random_id
from django.conf import settings


class Quotes(models.Model):
    quote_title = models.CharField(max_length=50, null=True, blank=True)
    quote_desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.CharField(max_length=8, primary_key=True,
                          default=generate_random_id)

    def __str__(self) -> str:
        return self.quote_desc

    def save(self, *args, **kwargs):
        # Only generate a new id if it's a new instance (i.e., not yet saved)
        if not self.id or not Quotes.objects.filter(id=self.id).exists():
            self.id = generate_random_id().lower()
            while Quotes.objects.filter(id=self.id).exists():
                self.id = generate_random_id().lower()

        super().save(*args, **kwargs)


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=50)
    quiz_desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='assigned_quiz', blank=True)
    id = models.CharField(max_length=8, primary_key=True,
                          default=generate_random_id)

    def __str__(self):
        return self.quiz_title

    def save(self, *args, **kwargs):
        if not self.id or not Quiz.objects.filter(id=self.id).exists():
            self.id = generate_random_id().lower()

            while Quiz.objects.filter(id=self.id).exists():
                self.id = generate_random_id().lower()

        super().save(*args, **kwargs)


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user} - {self.quiz} - Score: {self.score}"
