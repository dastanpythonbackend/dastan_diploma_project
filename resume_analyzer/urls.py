from django.urls import path
from rest_framework import permissions
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger UI для приложения
schema_view = get_schema_view(
    openapi.Info(
        title="Resume Analyzer API",  # Название API
        default_version='v1',  # Версия API
        description="API для анализа резюме",  # Описание API
        contact=openapi.Contact(email="support@resume_analyzer.local"),  # Контактная информация
    ),
    public=True,  # Указывает, что документация доступна для всех
    permission_classes=(permissions.AllowAny,),  # Разрешение на доступ для всех пользователей
)

# Определение URL-путей для приложения
urlpatterns = [
    # Путь для создания нового резюме
    path('resume_create/', views.ResumeCreateAPIView.as_view(), name='resume_create'),

    # Путь для отображения списка всех резюме
    path('resume_list/', views.ResumeListAPIView.as_view(), name='resume_list'),

    # Путь для получения детализированного анализа резюме
    path('resume_detail/', views.ResumeDetailView.as_view(), name='resume_detail'),

    # Путь для анализа резюме
    path('resume_analyze/<int:resume_id>/', views.ResumeAnalysisAPIView.as_view(), name='resume_analyze'),

    # Путь для получения отфильтрованного анализа резюме
    path('filtered_resume/<int:resume_id>/', views.FilteredResumeListView.as_view(), name='filtered_resume'),

    # Путь для доступа к Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),  # Swagger UI для resume_analyzer
]
