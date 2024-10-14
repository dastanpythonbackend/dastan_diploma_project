import requests
from requests import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from rest_framework import permissions, generics

# Create your views here.


class ResumeCreateAPIView(CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def analyze_resume(self, resume):
        print("analyze_resume")
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTg0Y2JiMTktMTgwMC00YmQyLWIzMmYtODAzNDU5OTBhNjY5IiwidHlwZSI6ImFwaV90b2tlbiJ9.41xKzG_GopHPulGmJBThBXz7DjonTiZK9iLS194uMo0"  # Замените на ваш токен
        }
        url = "https://api.edenai.run/v2/ocr/resume_parser"
        json_payload = {
            "providers": "openai",
        }

        with open(resume.file.path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, data=json_payload, headers=headers, files=files)

        if response.status_code == 200:
            result = response.json()
            # Обработайте результат и сохраните его в поле description
            resume.description = result  # Или выберите нужные поля из result
            resume.analyzed = True
            resume.save()
        else:
            # Обработайте ошибку, если необходимо
            print(f"Error analyzing resume: {response.text}")


class ResumeList(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ResumeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "Анализ заверщен!"})


class ResumeAnalysisAPIView(CreateAPIView):
    queryset = ResumeAnalysis.objects.all()
    serializer_class = ResumeAnalysisSerializer
