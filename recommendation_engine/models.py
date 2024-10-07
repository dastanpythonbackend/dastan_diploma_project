from django.db import models
from resume_analyzer.models import ResumeAnalysis

# Create your models here.


class Recommendation(models.Model):
    analysis = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='job_recommendations')
    recommended_jobs = models.TextField(blank=True, null=True)  # Список рекомендованных вакансий
    improvement_tips = models.TextField(blank=True, null=True)  # Рекомендации по улучшению резюме
    career_suggestions = models.TextField(blank=True, null=True)  # Рекомендации по карьерному развитию (курсы и т.п. то что проходил человек )
    created_at = models.DateTimeField(auto_now_add=True)
