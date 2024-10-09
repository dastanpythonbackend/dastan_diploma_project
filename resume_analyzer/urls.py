from django.urls import path
from .views import ResumeCreateAPIView, ResumeAnalysisAPIView

urlpatterns = [
    path('', ResumeCreateAPIView.as_view()),
    path('resume_analysis/', ResumeAnalysisAPIView.as_view())
]
