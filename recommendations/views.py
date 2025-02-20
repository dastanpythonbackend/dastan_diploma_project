import openai

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import ResumeAnalysis, Recommendation

openai.api_key = ()


def analyze_resume_view(request, resume_id):
    resume_analysis = get_object_or_404(ResumeAnalysis, id=resume_id)

    resume_description = (
        f'Name: {resume_analysis.name}\n'
        f'Email: {resume_analysis.email}\n'
        f'Phone: {resume_analysis.phone}\n'
        f'Education: {resume_analysis.education}\n'
        f'Experience: {resume_analysis.experience}\n'
        f'Skills: {resume_analysis.skills}\n'
        f'Certifications: {resume_analysis.certifications}'
    )

    resume_analysis_prompt = f'Это резюме с следующими деталями: {resume_description}.' \
                             'Дайте обратную связь по возможным улучшениям и предложите, как сделать его более впечатляющим.'

    job_recommendation_prompt = f'Это резюме с следующими деталями: {resume_description}.' \
                                'На основе данного резюме, порекомендуйте подходящие вакансии для кандидата.'

    career_advice_prompt = f'Это резюме с следующими деталями: {resume_description}.' \
                           'Предложите советы по развитию карьеры для кандидата, на основе этого резюме.'

    response_feedback = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': 'Вы эксперт по карьерному развитию, специализирующийся на улучшении резюме.'},
            {'role': 'user', 'content': resume_analysis_prompt},
        ],
        max_tokens=1000
    )

    response_job = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': 'Вы карьерный консультант и эксперт по подбору вакансий. Ваша задача — подбирать подходящие вакансии на основе опыта, навыков и квалификации кандидатов.'},
            {'role': 'user', 'content': job_recommendation_prompt},
        ],
        max_tokens=1000
    )

    response_career = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': 'Вы карьерный коуч и эксперт по профессиональному развитию. Ваша задача — предлагать рекомендации для карьерного роста, развития навыков и улучшения профессионального профиля.'},
            {'role': 'user', 'content': career_advice_prompt},
        ],
        max_tokens=1000
    )

    feedback = response_feedback['choices'][0]['message']['content'].strip()
    recommended_jobs = response_job['choices'][0]['message']['content'].strip()
    career_suggestions = response_career['choices'][0]['message']['content'].strip()

    feedback = feedback.replace('\n', ' ')
    recommended_jobs = recommended_jobs.replace('\n', ' ')
    career_suggestions = career_suggestions.replace('\n', ' ')

    recommendation = Recommendation.objects.create(
        resume=resume_analysis,
        improvement_tips=feedback,
        recommended_jobs=recommended_jobs,
        career_suggestions=career_suggestions
    )

    return JsonResponse({
        'status': 'success',
        'feedback': feedback,
        'recommended_jobs': recommended_jobs,
        'career_suggestions': career_suggestions,
        'recommendation_id': recommendation.id
    })
