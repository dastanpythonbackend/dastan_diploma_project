from django.urls import path
from rest_framework import permissions
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger UI для этого приложения
schema_view = get_schema_view(
    openapi.Info(
        title="Resume Analyzer API",
        default_version='v1',
        description="API для анализа резюме",
        contact=openapi.Contact(email="support@resume_analyzer.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('resume_create/', views.ResumeCreateAPIView.as_view(), name='resume_create'),
    path('resume_analyze/<int:resume_id>/', views.ResumeAnalysisAPIView.as_view(), name='resume_analyze'),
    path('filtered_resume/<int:resume_id>/', views.FilteredResumeListView.as_view(), name='filtered_resume'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),  # Swagger UI для resume_analyzer
]
