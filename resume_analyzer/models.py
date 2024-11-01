from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=True, null=True)  # Заголовок/название резюме
    description = models.JSONField(blank=True, null=True)  # Описание или краткий обзор резюме


class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    name = models.CharField(max_length=255, blank=True, null=True)  # Имя пользователя, извлеченное из резюме
    email = models.EmailField(blank=True, null=True)  # Контактный email
    phone = models.CharField(max_length=50, blank=True, null=True)  # Контактный телефон
    education = models.TextField(blank=True, null=True)  # Образование, выделенное из резюме
    experience = models.TextField(blank=True, null=True)  # Опыт работы
    skills = models.TextField(blank=True, null=True)  # Навыки
    certifications = models.TextField(blank=True, null=True)  # Сертификаты и достижения
    recommendations = models.TextField(blank=True, null=True)  # Рекомендации на основе анализа
    created_at = models.DateTimeField(auto_now_add=True)
    ai_content_detection = models.TextField(blank=True, null=True)
    emotion_detection = models.TextField(blank=True, null=True)
    pii_and_anonymization = models.TextField(blank=True, null=True)
    sentiment_analysis = models.TextField(blank=True, null=True)
