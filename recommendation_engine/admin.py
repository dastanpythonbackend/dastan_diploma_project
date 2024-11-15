from django.contrib import admin
from .models import Recommendation

# Регистрируем модель Recommendation в админке Django,
# чтобы можно было управлять записями рекомендаций через административный интерфейс.
admin.site.register(Recommendation)
