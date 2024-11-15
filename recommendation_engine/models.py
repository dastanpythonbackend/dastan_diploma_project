from django.db import models
from resume_analyzer.models import ResumeAnalysis


# Модель для хранения рекомендаций, основанных на анализе резюме
class Recommendation(models.Model):
    # Связь "многие к одному" с моделью ResumeAnalysis
    # Каждая рекомендация связана с конкретным анализом резюме
    resume = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='job_recommendations')

    # Рекомендованные рабочие вакансии, которые могут быть подходящими для пользователя
    # Это поле может быть пустым, если нет рекомендаций
    recommended_jobs = models.TextField(blank=True, null=True)

    # Советы по улучшению резюме или профессионального развития
    improvement_tips = models.TextField(blank=True, null=True)

    # Рекомендации по карьерному росту или смене профессии
    career_suggestions = models.TextField(blank=True, null=True)

    # Время создания рекомендации (устанавливается автоматически при создании записи)
    created_at = models.DateTimeField(auto_now_add=True)
