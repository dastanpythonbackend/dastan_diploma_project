from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ResumeAnalysis, Recommendation
import openai
import re

# API ключ
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
             "Дайте обратную связь по возможным улучшениям и предложите, как сделать его более впечатляющим." \
             "Также порекомендуйте вакансии, которые могут подойти для кандитата с такими навыками,"\
             \
             "и предложите советы по развитию карьеры для начинающего специалиста."

    # Отправляем запрос к GPT API
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Вы эксперт по карьерному развитию, специализирующийся на улучшении резюме."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    # Получаем результат анализа
    feedback = response["choices"][0]["message"]["content"].strip()

    # Используем регулярные выражения для извлечения разделов
    improvement_tips = ""
    recommended_jobs = ""
    career_suggestions = ""

    # Извлекаем "Рекомендации по улучшению резюме"
    match_feedback = re.search(r"Рекомендации по улучшению резюме:(.*?)(Примеры вакансий:|Советы по развитию карьеры:|$)", feedback, re.DOTALL)
    if match_feedback:
        improvement_tips = match_feedback.group(1).strip()

    # Извлекаем "Примеры вакансий"
    match_jobs = re.search(r"Примеры вакансий:(.*?)(Советы по развитию карьеры:|$)", feedback, re.DOTALL)
    if match_jobs:
        recommended_jobs = match_jobs.group(1).strip()

    # Извлекаем "Советы по развитию карьеры"
    match_career = re.search(r"Советы по развитию карьеры:(.*)", feedback, re.DOTALL)
    if match_career:
        career_suggestions = match_career.group(1).strip()

    # Если какие-то части не были найдены, подставляем дефолтные значения
    if not recommended_jobs:
        recommended_jobs = "Не были получены рекомендации по вакансиям."
    if not career_suggestions:
        career_suggestions = "Не были получены советы по карьере."

    # Заменить символы новой строки на пробелы для чистоты текста
    feedback = feedback.replace("\n", " ")
    improvement_tips = improvement_tips.replace("\n", " ")
    recommended_jobs = recommended_jobs.replace("\n", " ")
    career_suggestions = career_suggestions.replace("\n", " ")

    # Сохраняем рекомендации в базе данных
    recommendation = Recommendation.objects.create(
        resume=resume_analysis,
        improvement_tips=feedback,
        recommended_jobs=recommended_jobs,
        career_suggestions=career_suggestions
    )

    # Возвращаем JSON-ответ
    return JsonResponse({
        "status": "success",
        "feedback": feedback,
        "recommended_jobs": recommended_jobs,
        "career_suggestions": career_suggestions,
        "recommendation_id": recommendation.id
    })
