from rest_framework import serializers
from .models import Recommendation


# Сериализатор для модели Recommendation
class RecommendationSerializers(serializers.ModelSerializer):
    # Определяем поля, которые будут сериализованы и переданы в ответе API
    class Meta:
        model = Recommendation  # Указываем, что этот сериализатор связан с моделью Recommendation
        fields = ['recommended_jobs', 'improvement_tips', 'career_suggestions', 'created_at']   # Список полей модели, которые будут доступны в API
        read_only_fields = ['created_at']  # Указываем, что поле 'created_at' доступно только для чтения (не редактируется пользователем)
