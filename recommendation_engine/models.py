from django.db import models
from resume_analyzer.models import ResumeAnalysis

# Create your models here.


class Recommendation(models.Model):
    resume = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='job_recommendations')
    recommended_jobs = models.TextField(blank=True, null=True)
    improvement_tips = models.TextField(blank=True, null=True)
    career_suggestions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
