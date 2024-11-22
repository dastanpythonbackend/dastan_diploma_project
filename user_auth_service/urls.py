from django.urls import path
from rest_framework import permissions
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger UI для этого приложения.
schema_view = get_schema_view(
    openapi.Info(
        title="User Authentication Service API",  # Заголовок документации API
        default_version='v1',  # Версия API
        description="API для авторизации пользователей",  # Описание API
        contact=openapi.Contact(email="support@user_auth.local"),  # Контактный email
    ),
    public=True,  # Открытая документация
    permission_classes=(permissions.AllowAny,),  # Права доступа, доступно всем
)

urlpatterns = [
    # Путь для отображения Swagger UI (интерфейс для документации API).
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),

    # Путь для создания нового пользователя (регистрация).
    path('register/', views.ProfileView.as_view(), name='register'),

    # Путь для регистрации нового пользователя.
    path('registration_phone_number/', views.RegisterView.as_view(), name='registration_phone_number'),

    # Путь для верификации номера телефона через SMS.
    path('verify_sms/', views.VerifySMSView.as_view(), name='verify_sms'),
]
