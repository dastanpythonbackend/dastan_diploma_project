from django.urls import path
from .views import ResumeCreateAPIView, ResumeAnalysisAPIView, ResumeList

urlpatterns = [
    path('', ResumeCreateAPIView.as_view()),
    path('resume_analysis/', ResumeAnalysisAPIView.as_view()),
    path('resume_list/', ResumeList.as_view()),
]
