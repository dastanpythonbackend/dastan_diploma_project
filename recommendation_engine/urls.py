from django.urls import path
from . import views

urlpatterns = [
    path("recommendations/<int:resume_id>/recommendations/", views.ResumeRecommendationAPIView.as_view(), name="recommendations-create")
]
