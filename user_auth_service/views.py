from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from .serializers import ProfileSerializer
from .models import Profile


# Представление для создания нового пользователя
class ProfileView(generics.CreateAPIView):
    # Указывает на queryset пользователей, с которым будет работать данное представление.
    queryset = User.objects.all()

    # Сериализатор, который будет использоваться для преобразования данных.
    serializer_class = UserSerializer

    # Устанавливает права доступа: В данном случае доступ разрешен любому пользователю.
    permission_classes = (permissions.AllowAny,)


# Представление для регистрации пользователя с созданием профиля
class RegisterView(APIView):
    def post(self, request):
        # Получаем данные из запроса и валидируем их через сериализатор
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Сохраняем данные профиля в базу данных
        serializer.save()
        # Отправляем ответ с подтверждением, что код для проверки был отправлен
        return Response({"message": "Пользователь зарегистрирован. Код подтверждения отправлен через SMS."}, status=status.HTTP_201_CREATED)


# Представление для верификации номера телефона пользователя
class VerifySMSView(APIView):
    def post(self, request):
        # Получаем номер телефона и код из запроса
        phone_number = request.data.get('telephone')
        code = request.data.get('code')

        # Если отсутствуют телефон или код, генерируем ошибку валидации
        if not phone_number or not code:
            raise ValidationError({"error": "Телефон и код обязательны."})

        # Пытаемся найти профиль пользователя по номеру телефона
        try:
            profile = Profile.objects.get(telephone=phone_number)
        except Profile.DoesNotExist:
            # Если профиль не найден, генерируем ошибку
            raise NotFound({"error": "Пользователь не найден."})

        # Если код не совпадает с кодом из профиля, генерируем ошибку
        if profile.verification_token != code:
            raise ValidationError({"error": "Неверный код подтверждения."})

        # Если код правильный, помечаем профиль как проверенный и удаляем токен
        profile.verification = True
        profile.verification_token = None
        profile.save()

        # Отправляем успешный ответ о том, что номер телефона был успешно верифицирован
        return Response({"message": "Номер телефона успешно верифицирован."}, status=status.HTTP_200_OK)
