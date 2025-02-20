from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Resume, ResumeAnalysis


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]
        ref_name = 'ResumeAnalysisUserSerializer'


class ResumeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = ['file', 'uploaded_at', 'analyzed', 'title', 'description', 'user']
        read_only_fields = ['user', 'uploaded_at']


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ['resume', 'name', 'email', 'phone', 'education', 'experience', 'skills',
                  'certifications', 'recommendations', 'created_at', 'ai_content_detection', 'emotion_detection',
                  'pii_and_anonymization', 'sentiment_analysis']
