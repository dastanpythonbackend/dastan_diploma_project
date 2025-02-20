from django.urls import path
from . import views

urlpatterns = [
    path('resume-create/', views.ResumeCreateAPIView.as_view(), name='resume-create'),
    path('resume-list/', views.ResumeListAPIView.as_view(), name='resume-list'),
    path('resume-detail/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    path('resume-analysis/<int:resume_id>/', views.ResumeAnalysisAPIView.as_view(), name='resume-analysis'),
    path('filtered-resume/<int:resume_id>/', views.FilteredResumeListView.as_view(), name='filtered-resume'),
]
