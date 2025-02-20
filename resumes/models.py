from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.JSONField(blank=True, null=True)


class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ai_content_detection = models.TextField(blank=True, null=True)
    emotion_detection = models.TextField(blank=True, null=True)
    pii_and_anonymization = models.TextField(blank=True, null=True)
    sentiment_analysis = models.TextField(blank=True, null=True)
    extracted_data = models.JSONField(null=True, blank=True)
