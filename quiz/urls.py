from django.urls import path
from .views import QuotesView, QuizCreateView, QuizAssignView, UserAssignedQuizzesView, QuizDetailView, SubmitQuizResultView

urlpatterns = [
    path('qoutes/', QuotesView.as_view()),
    path('quiz/', QuizCreateView.as_view()),
    path('quiz/<int:pk>/', QuizCreateView.as_view()),
    path('assign-quiz/', QuizAssignView, name='quiz-assign'),
    path('get-quiz/', UserAssignedQuizzesView, name='user-assigned-quizzes'),
    path('get-quiz/<int:quiz_id>/', QuizDetailView, name='quiz-detail'),
    path('submit-quiz-result/', SubmitQuizResultView, name='submit-quiz-result'),
]
