from django.contrib import admin
from .models import Resume, ResumeAnalysis

# Регистрируем модель Resume в административной панели
# Это позволяет управлять записями модели Resume через админку Django
admin.site.register(Resume)

# Регистрируем модель ResumeAnalysis в административной панели
# Это позволяет управлять записями модели ResumeAnalysis через админку Django
admin.site.register(ResumeAnalysis)
