from django.db import models
from django.contrib.auth.models import User


# Модель профиля пользователя
class Profile(models.Model):
    # Связь один к одному с моделью User (пользователь системы)
    # Это означает, что у каждого пользователя может быть только один профиль
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Флаг, указывающий, подтвержден ли номер телефона пользователя
    verification = models.BooleanField(default=False)

    # Токен для подтверждения номера телефона
    verification_token = models.CharField(max_length=255, blank=True,null=True)

    # Счётчик попыток ввода кода подтверждения
    verification_count = models.IntegerField(default=0)

    # Телефонный номер пользователя
    telephone = models.CharField(max_length=20)

    # Поле для хранения роли пользователя в системе
    # Например: 'admin', 'moderator', 'user' и т. д.
    role = models.CharField(max_length=50)

    # Метод для строкового представления объкта профиля
    # Возвращаем имя пользователя, связанного с этим профилем
    def __str__(self):
        return self.user.username
