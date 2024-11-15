from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Resume, ResumeAnalysis


# Сериализатор для модели User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Модель пользователя Django
        fields = ['id', 'username', 'email',]  # Указываем, какие поля модели пользователя должны быть включены в сериализатор
        ref_name = 'ResumeAnalyzerUserSerializer'  # Уникальное имя для этого сериализатора. Это полезно, если есть несколько сериализаторов одной модели в разных контекстах


# Сериализатор для модели Resume
class ResumeSerializer(serializers.ModelSerializer):
    # Включаем данные пользователя, связанного с резюме, в виде сериализатора UserSerializer.
    # Указываем read_only=True, чтобы данные о пользователе были только для чтения (не изменялись при обновлении резюме)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Resume  # Указываем модель Resume
        fields = ['file', 'uploaded_at', 'analyzed', 'title', 'description', 'user']
        # Указываем, что поля 'user' и 'uploaded_at' должны быть только для чтения
        read_only_fields = ['user', 'uploaded_at']


# Сериализатор для модели ResumeAnalysis
class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis  # Указываем модель ResumeAnalysis
        # Определяем, какие поля модели ResumeAnalysis должны быть сериализованы
        fields = ['resume', 'name', 'email', 'phone', 'education', 'experience', 'skills',
                  'certifications', 'recommendations', 'created_at', 'ai_content_detection', 'emotion_detection',
                  'pii_and_anonymization', 'sentiment_analysis']
