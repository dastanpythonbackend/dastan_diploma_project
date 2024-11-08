from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ResumeAnalysis, Recommendation
import openai

# Установите ваш API ключ
openai.api_key = ()


def analyze_resume_view(request, resume_id):
    # Получаем резюме из базы данных
    resume_analysis = get_object_or_404(ResumeAnalysis, id=resume_id)

    # Формируем описание резюме
    resume_description = (
        f"Name: {resume_analysis.name}\n"
        f"Email: {resume_analysis.email}\n"
        f"Phone: {resume_analysis.phone}\n"
        f"Education: {resume_analysis.education}\n"
        f"Experience: {resume_analysis.experience}\n"
        f"Skills: {resume_analysis.skills}\n"
        f"Certifications: {resume_analysis.certifications}"
    )

    # Формируем текстовый запрос на русском языке для анализа и улучшения резюме
    prompt = f"Это резюме с следующими деталями: {resume_description}. " \
             "Дайте обратную связь по возможным улучшениям и предложите, как сделать его более впечатляющим."

    # Отправляем запрос к GPT API
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Вы эксперт по карьерному развитию, специализирующийся на улучшении резюме."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=255
    )

    # Получаем результат анализа
    feedback = response['choices'][0]['message']['content'].strip()

    # Сохраняем рекомендации в базе данных
    recommendation = Recommendation.objects.create(
        resume=resume_analysis,
        recommended_jobs="Пример предложенных вакансий...",
        improvement_tips=feedback,
        career_suggestions="Советы по развитию карьеры..."
    )

    # Возвращаем JSON-ответ
    return JsonResponse({
        "status": "success",
        "feedback": feedback,
        "recommendation_id": recommendation.id
    })
