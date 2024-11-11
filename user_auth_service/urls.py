from django.urls import path
from rest_framework import permissions
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger UI для этого приложения.
schema_view = get_schema_view(
    openapi.Info(
        title="User Authentication Service API",
        default_version='v1',
        description="API для авторизации пользователей",
        contact=openapi.Contact(email="support@user_auth.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Эндпоинт для создания нового пользователя.
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Эндпоинт Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
]
