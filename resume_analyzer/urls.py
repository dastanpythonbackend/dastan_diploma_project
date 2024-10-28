from django.urls import path
from .views import ResumeCreateAPIView, ResumeListAPIView, ResumeDetailView, analyze_resume_view

urlpatterns = [
    path('', ResumeCreateAPIView.as_view()),
    path('resume_list/', ResumeListAPIView.as_view()),
    path('resume_detail/', ResumeDetailView.as_view()),
    path('analyze_resume/<int:resume_id>/', analyze_resume_view, name='analyze_resume'),
]
