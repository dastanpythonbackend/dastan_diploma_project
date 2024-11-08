import openai
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Recommendation
from .serializers import RecommendationSerializers
from resume_analyzer.models import ResumeAnalysis

openai.api_key = ''


class ResumeRecommendationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, resume_id):
        try:
            # Получаем анализ резюме по ID
            resume_analysis = ResumeAnalysis.objects.get(analysis=resume_id)

            # Извлекаем данные для анализа
            extracted_data = resume_analysis.extracted_data

            # Генерация рекомендаций
            recommendations_text = self.generate_recommendations(extracted_data)

            # Создаем объект Recommendation
            recommendation = Recommendation.objects.create(
                resume=resume_analysis.resume,
                recommendations_text=recommendations_text
            )

            # Сериализуем результат
            serializer = RecommendationSerializers(recommendation)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ResumeAnalysis.DoesNotExist:
            return Response({"error": "Resume analysis not found."}, status=status.HTTP_404_NOT_FOUND)

    def generate_recommendations(self, extracted_data):
        skills = ", ".join([skill.get("name", "") for skill in extracted_data.get("skills", [])])
        experience = " ".join(
            [entry.get("description", "") for entry in extracted_data.get("work_experience", {}).get("entries", [])])

        prompt = f"""
        Based on the skills: {skills} and experience: {experience}, generate recommendations for career growth, job opportunities, and skills to focus on.
        """

        try:
            # Используем OpenAI API для генерации рекомендаций
            response = openai.Completion.create(
                model="gpt-4o",
                engine="text-davinci-003",  # Выберите нужную модель
                prompt=prompt,
                max_tokens=255
            )

            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
