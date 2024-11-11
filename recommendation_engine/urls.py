# recommendation_engine/urls.py
from django.urls import path
from rest_framework import permissions

from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger UI для этого приложения
schema_view = get_schema_view(
    openapi.Info(
        title="Recommendation Engine API",
        default_version='v1',
        description="API для генерации рекомендаций",
        contact=openapi.Contact(email="support@recommendation_engine.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('analyze-resume/<int:resume_id>/', views.analyze_resume_view, name='analyze_resume'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),  # Swagger UI для recommendation_engine
]
