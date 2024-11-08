from rest_framework import serializers
from .models import Recommendation


class RecommendationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['recommended_jobs', 'improvement_tips', 'career_suggestions']
        read_only_fields = ['created_at']
