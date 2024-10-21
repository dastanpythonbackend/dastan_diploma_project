import requests
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from rest_framework import permissions, generics
from django.http import JsonResponse

# Create your views here.


class ResumeCreateAPIView(CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):

        if self.request.user.is_anonymous:
            raise NotAuthenticated("User must be authenticated to upload a resume.")

        resume = serializer.save(user=self.request.user)

        self.analyze_resume(resume)

    def analyze_resume(self, resume):
        print("analyze_resume started")
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw"
        }
        url = "https://api.edenai.run/v2/ocr/resume_parser"
        json_payload = {
            "providers": "openai",
        }

        try:
            with open(resume.file.path, "rb") as f:
                files = {"file": f}
                response = requests.post(url, data=json_payload, headers=headers, files=files)

            if response.status_code == 200:
                result = response.json()
                resume.description = result
                resume.analyzed = True
                resume.save()
                print("Resume analyzed and saved successfully.")
            else:
                print(f"Error analyzing resume: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception while analyzing resume: {e}")


class ResumeList(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ResumeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "Анализ заверщен!"})


class ResumeAnalysisAPIView(APIView):
    queryset = ResumeAnalysis.objects.all()
    serializer_class = ResumeAnalysisSerializer


class ResumeAnalyzer:
    def __init__(self, resume_id):
        # Инициализация объекта Resume по ID
        self.resume = get_object_or_404(Resume, id=resume_id)
        self.json_data = self.resume.description  # Извлечение JSON-данных из поля description

    def extract_and_save_analysis(self):

        extracted_data = self.json_data.get("openai", {}).get("extracted_data", {})
        personal_info = extracted_data.get("personal_infos", {})
        education_info = extracted_data.get("education", {})
        work_experience = extracted_data.get("work_experience", {})

        # Сохранение данных в модель ResumeAnalysis
        ResumeAnalysis.objects.update_or_create(
            resume=self.resume,
            defaults={
                "name": personal_info.get("name", {}).get("raw_name"),
                "email": personal_info.get("mails", [None])[0],
                "phone": personal_info.get("phones", [None])[0],
                "education": str(education_info),
                "experience": str(work_experience),
                "skills": ", ".join([skill.get("name") for skill in extracted_data.get("skills", [])]),
                "certifications": str(extracted_data.get("certifications", [])),
                "recommendations": extracted_data.get("recommendations", "")
            }
        )

        self.resume.analyzed = True
        self.resume.save()

        return {"status": "успех", "message": "реюме обработанно"}


def analyze_resume_view(request, resume_id):
    analyzer = ResumeAnalyzer(resume_id)
    result = analyzer.extract_and_save_analysis()

    return JsonResponse(result)
