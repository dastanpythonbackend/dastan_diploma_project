from django.urls import path
from . import views

urlpatterns = [
    path('analyze-resume/<int:resume_id>/', views.analyze_resume_view, name='analyze-resume'),
]
