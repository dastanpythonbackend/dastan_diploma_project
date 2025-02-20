from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.ProfileView.as_view(), name='register'),
    path('registration-phone-number/', views.RegisterView.as_view(), name='registration-phone-number'),
    path('verify-sms/', views.VerifySMSView.as_view(), name='verify-sms'),
]
