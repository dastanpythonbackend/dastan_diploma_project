from django.db import models  # Импорт моделей Django
from django.contrib.auth.models import User  # Импорт модели пользователя Django


# Модель для резюме
class Resume(models.Model):
    # Связь с пользователем, который загрузил резюме
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Поле для хранения файла резюме
    file = models.FileField(upload_to='resumes/')
    # Поле для хранения даты и времени загрузки резюме, автоматически устанавливается при добавлении
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Флаг, который указывает, было ли резюме проанализировано
    analyzed = models.BooleanField(default=False)
    # Заголовок резюме
    title = models.CharField(max_length=255, blank=True, null=True)
    # Описание или краткий обзор резюме, сохраняется в формате JSON
    description = models.JSONField(blank=True, null=True)


# Модель для анализа резюме
class ResumeAnalysis(models.Model):
    # Связь с моделью Resume, один анализ на одно резюме
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    # Извлеченное имя из резюме
    name = models.CharField(max_length=255, blank=True, null=True)
    # Извлеченный email из резюме
    email = models.EmailField(blank=True, null=True)
    # Извлеченный телефон из резюме
    phone = models.CharField(max_length=50, blank=True, null=True)
    # Извлеченное образование из резюме
    education = models.TextField(blank=True, null=True)
    # Извлеченный опыт работы из резюме
    experience = models.TextField(blank=True, null=True)
    # Извлеченные навыки из резюме
    skills = models.TextField(blank=True, null=True)
    # Извлеченные сертификаты и достижения из резюме
    certifications = models.TextField(blank=True, null=True)
    # Рекомендации, сформированные на основе анализа резюме
    recommendations = models.TextField(blank=True, null=True)
    # Дата и время создания анализа
    created_at = models.DateTimeField(auto_now_add=True)
    # Результаты анализа контента с помощью ИИ
    ai_content_detection = models.TextField(blank=True, null=True)
    # Результаты анализа эмоций
    emotion_detection = models.TextField(blank=True, null=True)
    # Результаты анонимизации и анализа персональных данных
    pii_and_anonymization = models.TextField(blank=True, null=True)
    # Результаты анализа настроений
    sentiment_analysis = models.TextField(blank=True, null=True)
    # Извлеченные данные, сохраненные в формате JSON
    extracted_data = models.JSONField(null=True, blank=True)
