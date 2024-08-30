from rest_framework import serializers
from .models import Quotes, Quiz, Question, Option


class QuotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = ['id', 'quote_title', 'qoute_desc', 'qoute_id',
                  'created_at', 'updated_at']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']

    def create(self, validated_data):
        return Option.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.option_text = validated_data.get(
            'option_text', instance.option_text)
        instance.is_correct = validated_data.get(
            'is_correct', instance.is_correct)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'question', 'options']

    def validate_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(
                "Each question must have exactly 4 options.")
        return value

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.save()

        options_data = validated_data.get('options', [])
        existing_option_ids = [option.id for option in instance.options.all()]

        # Update existing options or create new ones
        for option_data in options_data:
            option_id = option_data.get('id')
            if option_id in existing_option_ids:
                option = Option.objects.get(id=option_id, question=instance)
                option.option_text = option_data.get(
                    'option_text', option.option_text)
                option.is_correct = option_data.get(
                    'is_correct', option.is_correct)
                option.save()
            else:
                Option.objects.create(question=instance, **option_data)

        # Remove options that were not included in the update request
        for option_id in existing_option_ids:
            if option_id not in [data.get('id') for data in options_data]:
                Option.objects.get(id=option_id, question=instance).delete()

        return instance


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

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

    def update(self, instance, validated_data):
        instance.quiz_title = validated_data.get(
            'quiz_title', instance.quiz_title)
        instance.quiz_desc = validated_data.get(
            'quiz_desc', instance.quiz_desc)
        instance.save()

        questions_data = validated_data.get('questions', [])
        existing_question_ids = [
            question.id for question in instance.questions.all()]

        # Update existing questions or create new ones
        for question_data in questions_data:
            question_id = question_data.get('id')
            if question_id in existing_question_ids:
                question = Question.objects.get(id=question_id, quiz=instance)
                question_serializer = QuestionSerializer(
                    question, data=question_data, partial=True)
                if question_serializer.is_valid():
                    question_serializer.save()
                else:
                    raise serializers.ValidationError(
                        question_serializer.errors)
            else:
                options_data = question_data.pop('options')
                question = Question.objects.create(
                    quiz=instance, **question_data)
                for option_data in options_data:
                    Option.objects.create(question=question, **option_data)

        # Remove questions that were not included in the update request
        for question_id in existing_question_ids:
            if question_id not in [data.get('id') for data in questions_data]:
                Question.objects.get(id=question_id, quiz=instance).delete()

        return instance
