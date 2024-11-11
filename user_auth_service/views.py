from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer


# Представление для создания нового пользователя
class ProfileView(generics.CreateAPIView):
    # Указывает на queryset пользователей, с которым будет работать данное представление.
    queryset = User.objects.all()

    # Сериализатор, который будет использоваться для преобразования данных.
    serializer_class = UserSerializer

    # Устанавливает права доступа: В данном случае доступ разрещён любому пользователю.
    permission_classes = (permissions.AllowAny,)
