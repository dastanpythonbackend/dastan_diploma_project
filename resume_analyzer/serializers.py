from rest_framework import serializers
from .models import Resume, ResumeAnalysis

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['file', 'uploaded_at', 'analyzed', 'title', 'description']

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ['resume', 'name', 'email', 'phone', 'education', 'experience', 'skills',
                  'certifications', 'recommendations', 'created_at']
