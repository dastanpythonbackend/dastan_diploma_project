from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
import random
from twilio.rest import Client
from django.conf import settings


# Сериализатор для модели User, включая поля для пароля
class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)  # Пароль, который будет введен пользователем
    password2 = serializers.CharField(write_only=True)  # Повтор пароля для проверки

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Указываем поля модели, которые будут использоваться в сериализаторе
        extra_kwargs = {
            'username': {'write_only': True},   # Поле username только для записи (не выводится в ответе)
            'email': {'write_only': True}   # Поле email только для записи (не выводится в ответе)
        }

    # Метод для создания пользователя с проверкой совпадения паролей
    def create(self, validated_data):
        password1 = validated_data.pop('password1')  # Извлекаем первый пароль
        password2 = validated_data.pop('password2')  # Извлекаем второй пароль для проверки
        if password1 != password2:
            raise serializers.ValidationError({"error": "Пароли не совпадают."})  # Проверяем, что пароли совпадают
        user = User(**validated_data)   # Создаем объект пользователя
        user.set_password(password1)  # Хэшируем пароль
        user.save()  # Сохраняем пользователя в базе данных
        return user  # Возвращаем созданного пользователя


# Сериализатор для модели Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Включаем сериализатор пользователя для связи с профилем

    class Meta:
        model = Profile
        fields = ['user', 'telephone', 'verification', 'role']  # Указываем поля, которые будут использоваться
        extra_kwargs = {'verification': {'read_only': True}}  # Поле verification доступно только для чтения

    # Метод для создания профиля с верификацией и отправкой SMS
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Извлекаем данные для пользователя
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)  # Создаем пользователя через UserSerializer
        verification_code = generate_verification_code()  # Генерируем код верификации

        # Создаем объект профиля
        profile = Profile.objects.create(
            user=user,
            telephone=validated_data['telephone'],  # Привязываем номер телефона
            verification_token=verification_code,  # Сохраняем код для верификации
            role=validated_data.get('role', 'user')   # Присваиваем роль, если она указана
        )

        send_verification_sms(profile.telephone, verification_code)  # Отправка SMS с кодом верификации
        return profile  # Возвращаем созданный профиль


# Функция для генерации случайного шестизначного кода верификации
def generate_verification_code():
    return str(random.randint(100000, 999999))  # Генерирует случайный код от 100000 до 999999


# Функция для отправки SMS с кодом верификации
def send_verification_sms(phone_number, code):
    account_sid = settings.TWILIO_ACCOUNT_SID  # Получаем SID аккаунта Twilio из настроек
    auth_token = settings.TWILIO_AUTH_TOKEN  # Получаем токен авторизации из настроек
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER  # Получаем номер телефона Twilio из настроек

    client = Client(account_sid, auth_token)   # Инициализация клиента Twilio с использованием SID и токена
    try:
        # Отправка SMS через Twilio
        message = client.messages.create(
            body=f"Your verification code is: {code}",  # Текст SMS с кодом верификации
            from_=twilio_phone_number,  # Отправитель (номер Twilio)
            to=phone_number  # Получатель (номер телефона пользователя)
        )
        print(f"SMS sent to {phone_number}. SID: {message.sid}")  # Логируем успешную отправку
    except Exception as e:
        print(f"Failed to send SMS: {e}")  # Логируем ошибку, если отправка не удалась
        raise Exception("Failed to send SMS")  # Выбрасываем исключение, если отправка не удалась
