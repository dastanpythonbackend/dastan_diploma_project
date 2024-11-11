from django.contrib import admin
from .models import Profile

# Регистрируем модель Profile в админке Django,
# чтобы можно было управлять профилями пользователей через интерфейс администратора.
admin.site.register(Profile)
