from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Quotes
from .serializer import QuotesSerializer, QuizSerializer
from .models import *


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
