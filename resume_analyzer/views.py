import requests
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from rest_framework import permissions, generics
import json

# Create your views here.


class ResumeCreateAPIView(CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class ResumeListAPIView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResumeDetailView(generics.RetrieveAPIView):
    queryset = ResumeAnalysis.objects.all()
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResumeAnalyzer:
    def __init__(self, resume_id):
        # Инициализация объекта Resume по ID
        self.resume = get_object_or_404(Resume, id=resume_id)
        self.json_data = self._get_json_data()

    def _get_json_data(self):
        if self.resume.description:
            try:
                return json.loads(self.resume.description)
            except json.JSONDecodeError:
                return {}
        return {}

    def extract_and_save_analysis(self):
        extracted_data = self.json_data.get("openai", {}).get("extracted_data", {})
        print("extracted_data", extracted_data)
        personal_info = extracted_data.get("personal_info", {})
        print("personal_info", personal_info)
        education_info = extracted_data.get("education", {})
        work_experience = extracted_data.get("work_experience", {})

        # Сохранение данных в модель ResumeAnalysis
        analysis, _ = ResumeAnalysis.objects.update_or_create(
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
        print("analysis", analysis)
        return analysis

    def ai_content_detection(self, text):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw", "Content-Type": "application/json"}

        url = "https://api.edenai.run/v2/text/ai_detection"
        payload = {
            "providers": "originalityai",
            "text": text,
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()

    def emotion_detection(self, text):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw", "Content-Type": "application/json"}

        url = "https://api.edenai.run/v2/text/emotion_detection"
        payload = {
            "providers": "nlpcloud,vernai",
            "text": text,
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()

    def pii_and_anonymization(self, text):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw", "Content-Type": "application/json"}

        url = "https://api.edenai.run/v2/text/anonymization"
        payload = {
            "providers": "emvista",
            "language": "en",
            "text": text,
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()

    def question_answer(self):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw", "Content-Type": "application/json"}

        url = "https://api.edenai.run/v2/image/question_answer"
        json_payload = {
            "providers": "alephalpha",
            "file_url": "🔗 URL of your image",
            "question": "What are the logos on the image ?",
        }

        response = requests.post(url, json=json_payload, headers=headers)

        return response.json()

    def sentiment_analysis(self, text):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw", "Content-Type": "application/json"}

        url = "https://api.edenai.run/v2/text/sentiment_analysis"
        payload = {
            "providers": "google,amazon",
            "language": "en",
            "text": text,
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()


def analyze_resume_view(request, resume):
    try:
        analyzer = ResumeAnalyzer(resume.id)

        analysis = analyzer.extract_and_save_analysis()
        text_to_analyze = analysis.education

        # Выполняем анализ текста с помощью различных методов
        ai_content_detection = analyzer.ai_content_detection(text_to_analyze)
        emotion_detection = analyzer.emotion_detection(text_to_analyze)
        pii_and_anonymization = analyzer.pii_and_anonymization(text_to_analyze)
        sentiment_analysis = analyzer.sentiment_analysis(text_to_analyze)

        # Сохраняем результаты анализа в JSON-формате
        analysis.ai_content_detection = json.dumps(ai_content_detection)
        analysis.emotion_detection = json.dumps(emotion_detection)
        analysis.pii_and_anonymization = json.dumps(pii_and_anonymization)
        analysis.question_answer = json.dumps(question_answer)
        analysis.sentiment_analysis = json.dumps(sentiment_analysis)

        # Сохраняем изменения в базе данных
        analysis.save()

        # Отмечаем резюме как проанализированное
        resume.analyzed = True
        resume.save()

        print("Resume analyzed and saved succesfully.")
    except Exception as e:
        print(f"Exception while analyzing resume: {e}")
