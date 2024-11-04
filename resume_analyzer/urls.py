from django.urls import path
from . import views

urlpatterns = [
    # Эндпоинт для создания резюме

    path('resumes/create/', views.ResumeCreateAPIView.as_view(), name='resume-create'),

    # Эндпоинт для списка всех резюме

    path('resumes/', views.ResumeListAPIView.as_view(), name='resume-list'),

    # Эндпоинт для просмотра деталей анализа резюме

    path('resumes/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),

    # Эндпоинт для запуска анализа по определенному ID резюме
    path('resumes/<int:resume_id>/analyze/', views.ResumeAnalysisAPIView.as_view(), name='resume-analyze'),

    # Эндпоинт для получения нужных данных
    path('resumes/<int:resume_id>/filtered_resume/', views.FilteredResumeListView.as_view(), name='filtered_resume'),
]
