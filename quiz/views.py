from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Quotes
from .serializer import QuotesSerializer, QuizSerializer
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class QuotesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        quote_title = request.data.get('quote_title')
        quote_desc = request.data.get('quote_desc')

        if not all([quote_title, quote_desc]):
            return Response({"error": "Both title and description are required."}, status=status.HTTP_400_BAD_REQUEST)

        quote = Quotes(
            quote_title=quote_title,
            qoute_desc=quote_desc,
            created_by=request.user
        )
        quote.save()

        return Response({
            "success": "Quote created successfully.",
            "quote": QuotesSerializer(quote).data
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        quotes = Quotes.objects.filter(created_by=request.user)
        serializer = QuotesSerializer(quotes, many=True)

        return Response({"quotes": serializer.data}, status=status.HTTP_200_OK)


class QuizCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        if pk is None:
            quizzes = Quiz.objects.all()
            serializer = QuizSerializer(quizzes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                quiz = Quiz.objects.get(pk=pk)
            except Quiz.DoesNotExist:
                return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def QuizAssignView(request):
    user_id = request.data.get('user_id')
    quiz_id = request.data.get('quiz_id')

    if not user_id or not quiz_id:
        return Response({"error": "Both 'user_id' and 'quiz_id' are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, id=user_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if user in quiz.assigned_users.all():
        return Response({"error": "User is already assigned to this quiz."}, status=status.HTTP_400_BAD_REQUEST)

    quiz.assigned_users.add(user)
    quiz.save()

    return Response({"success": "User assigned to quiz successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserAssignedQuizzesView(request):
    user = request.user
    quizzes = Quiz.objects.filter(assigned_users=user)
    if not quizzes.exists():
        return Response({"message": "No quizzes assigned to you."}, status=status.HTTP_404_NOT_FOUND)

    quiz_data = [
        {
            "quiz_id": quiz.id,
            "quiz_title": quiz.quiz_title,
            "quiz_desc": quiz.quiz_desc
        }
        for quiz in quizzes
    ]
    return Response({"quizzes": quiz_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def QuizDetailView(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if user not in quiz.assigned_users.all():
        return Response({"error": "You do not have permission to access this quiz."}, status=status.HTTP_403_FORBIDDEN)
    serializer = QuizSerializer(quiz)
    return Response({"quiz": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SubmitQuizResultView(request):
    user = request.user
    quiz_id = request.data.get('quiz_id')
    score = request.data.get('score')

    if not quiz_id or score is None:
        return Response({"error": "Both 'quiz_id' and 'score' are required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        score = float(score)
    except ValueError:
        return Response({"error": "Score must be a numeric value."}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    if user not in quiz.assigned_users.all():
        return Response({"error": "You do not have permission to submit results for this quiz."}, status=status.HTTP_403_FORBIDDEN)

    result, created = UserQuizResult.objects.update_or_create(
        user=user,
        quiz=quiz,
        defaults={'score': score}
    )

    return Response({"success": "Quiz result submitted successfully.", "score": result.score}, status=status.HTTP_201_CREATED)
