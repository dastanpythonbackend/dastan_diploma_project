from django.urls import path
from rest_framework import permissions
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger UI для приложения
schema_view = get_schema_view(
    openapi.Info(
        title="Recommendation Engine API",  # Название API
        default_version='v1',  # Версия API
        description="API для генерации рекомендаций",  # Описание API
        contact=openapi.Contact(email="support@recommendation_engine.local"),  # Контактная информация
    ),
    public=True,  # Указывает, что документация доступна для всех
    permission_classes=(permissions.AllowAny,),  # Разрешение на доступ для всех пользователей
)

urlpatterns = [
    # Путь для анализа резюме и генерации рекомендаций
    # Параметр resume_id используется для извлечения данных конкретного резюме
    path('analyze_resume/<int:resume_id>/', views.analyze_resume_view, name='analyze_resume'),

    # Путь для доступа к Swagger UI для документации API
    # Swagger UI позволяет пользователям видеть и взаимодействовать с API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
