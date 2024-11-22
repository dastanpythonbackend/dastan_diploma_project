"""
URL configuration for diploma_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Получение клиентского ID и секретного ключа для Google OAuth из настроек проекта
GOOGLE_CLIENT_ID = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
GOOGLE_CLIENT_SECRET = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']

# URL редиректа, который будет использоваться для ответа от Google
REDIRECT_URI = "https://3f0c-31-192-250-102.ngrok-free.app/api/auth/google/callback/"


# Класс для обработки запроса на авторизацию через Google
class GoogleLoginView(APIView):
    def get(self, request):
        # Строим URL для запроса авторизации у Google с необходимыми параметрами
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={GOOGLE_CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid email profile&"
            f"prompt=consent"
        )
        # Перенаправляем пользователя на страницу авторизации Google
        return redirect(auth_url)


# Класс для обработки колбэка от Google после авторизации
class GoogleAuthCallbackView(APIView):
    # Извлекаем код авторизации из URL
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Получение access_token от Google с использованием authorization code
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        # Отправляем запрос на получение токена
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        # Проверяем наличие access_token в ответе
        access_token = token_json.get("access_token")
        if not access_token:
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

        # Используем полученный access_token для получения информации о пользователе
        userinfo_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
        userinfo_response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = userinfo_response.json()

        # Проверяем успешность получения данных о пользователе
        if userinfo_response.status_code != 200:
            return Response({"error": "Failed to fetch user info from Google"}, status=status.HTTP_400_BAD_REQUEST)

        # Отправляем полученную информацию (email и name) в ответ
        return Response({
            "email": user_info.get("email"),
            "name": user_info.get("name"),
        })


urlpatterns = [
    # Административный интерфейс Django
    path('admin/', admin.site.urls),

    # Включение URL-ов приложения user_auth_service (например, аутентификация)
    path('auth/', include('user_auth_service.urls')),

    # Включение URL-ов для приложения resume_analyzer (например, анализ резюме)
    path('resumes/', include('resume_analyzer.urls')),

    # Включение URL-ов для приложения recommendation_engine (например, рекомендации)
    path('recommendations/', include('recommendation_engine.urls')),

    # Эндпоинты для получения JWT токенов (обновление и получение пары токенов)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Включение URL-ов для dj_rest_auth (обработка JWT эндпоинтов)
    path('auth/', include('dj_rest_auth.urls')),

    # Включение URL-ов для регистрации пользователей с использованием dj_rest_auth
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    # Включение URL-ов для обработки авторизации через социальные сети, в том числе Google
    path('auth/social/', include('allauth.socialaccount.urls')),

    # Эндпоинты для авторизации через Google
    path('api/auth/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('api/auth/google/callback/', GoogleAuthCallbackView.as_view(), name='google_callback'),
]

# Статические файлы (только в режиме отладки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
