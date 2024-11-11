from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


# Сериализатор для модели Profile (профиль пользователя)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile  # Модель, для которой создаётся сериализатор
        fields = ['role']  # Сериализуемое поле: роль пользоателя в системе


# Сериализатор для модели User (пользователь системы)
class UserSerializer(serializers.ModelSerializer):
    # Вложенный сериалиэатор для связи с моделью Profile
    profile = ProfileSerializer()

    class Meta:
        model = User  # Модель, для которой создаётся сериализатор
        fields = ['username', 'email', 'password', 'profile']  # Поля модели User, которые сериализуем
        ref_name = 'UserAuthServiceUserSerializer'  # Уникальное имя сериализатора для этого контекста

    # Метод для создания пользователя и его профиля
    def create(self, validated_data):
        # Извлекаем данные профиля из validated_data
        profile_data = validated_data.pop('profile')

        # Создаём пользователя с данными, полученными из validated_data
        user = User.objects.create(**validated_data)

        # Создаём профиль пользователя, связывая его с только что созданным пользователем
        Profile.objects.create(user=user, **profile_data)

        # Возвращаем созданного пользователя
        return user
