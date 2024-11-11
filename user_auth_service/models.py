from django.db import models
from django.contrib.auth.models import User


# Модель профиля пользователя
class Profile(models.Model):
    # Связь один к одному с моделью User (пользователь системы)
    # Это означает, что у каждого пользователя может быть только один профиль
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Поле для хранения роли пользователя в системе
    # Например: 'admin', 'moderator', 'user' и т. д.
    role = models.CharField(max_length=50)

    # Метод для строкового представления объкта профиля
    # Возвращаем имя пользователя, связанного с этим профилем
    def __str__(self):
        return self.user.username
