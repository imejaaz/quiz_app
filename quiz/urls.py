from django.urls import path
from .views import QuotesView, QuizCreateView

urlpatterns = [
    path('qoutes/', QuotesView.as_view()),
    path('quiz/', QuizCreateView.as_view()),
    path('quiz/<int:pk>/', QuizCreateView.as_view())
]
