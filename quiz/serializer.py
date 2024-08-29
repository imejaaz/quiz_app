from rest_framework import serializers
from .models import Quotes, Quiz, Question, Option


class QuotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = ['id', 'quote_title', 'qoute_desc',
                  'created_at', 'updated_at']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'options']

    def validate_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(
                "Each question must have exactly 4 options.")
        return value


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=True)

    class Meta:
        model = Quiz
        fields = ['id', 'quiz_title', 'quiz_desc', 'questions']

    def validate_questions(self, value):
        if not (1 <= len(value) <= 4):
            raise serializers.ValidationError(
                "A quiz must have between 1 to 4 questions.")
        return value

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = Question.objects.create(quiz=quiz, **question_data)
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)
        return quiz
