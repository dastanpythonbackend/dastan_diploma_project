from django.urls import path
from .views import ResumeCreateAPIView, ResumeAnalysisAPIView, ResumeList, analyze_resume_view

urlpatterns = [
    path('', ResumeCreateAPIView.as_view()),
    path('resume_analysis/', ResumeAnalysisAPIView.as_view()),
    path('resume_list/', ResumeList.as_view()),
    path('analyze_resume/<int:resume_id>/', analyze_resume_view, name='analyze_resume'),
]
