import requests
import json
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer


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


class ResumeAnalysisAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, resume_id):
        resume = get_object_or_404(Resume, id=resume_id)

        # Извлечение данных из JSON, который находится в поле description
        description_data = resume.description
        if not description_data:
            return Response({"error": "Description data is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Пример извлечения нужного текста для анализа
        try:
            extracted_data = description_data.get("openai", {}).get("extracted_data", {})
            personal_info = extracted_data.get("personal_infos", {})
            text_for_analysis = f"{personal_info.get('self_summary', '')} {personal_info.get('objective', '')}"
            if not text_for_analysis.strip():
                text_for_analysis = " ".join([entry.get("description", "") for entry in
                                              extracted_data.get("work_experience", {}).get("entries", [])])
        except Exception as e:
            return Response({"error": f"Failed to extract text for analysis: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Выполнение анализа с использованием извлеченного текста
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw"
        }

        ai_content_detection = self.ai_content_detection(text_for_analysis, headers)
        emotion_detection = self.emotion_detection(text_for_analysis, headers)
        pii_and_anonymization = self.pii_and_anonymization(text_for_analysis, headers)
        sentiment_analysis = self.sentiment_analysis(text_for_analysis, headers)

        # Сохранение результатов анализа в базу данных
        analysis, created = ResumeAnalysis.objects.update_or_create(
            resume=resume,
            defaults={
                "name": personal_info.get("name", {}).get("raw_name"),
                "email": personal_info.get("mails", [None])[0],
                "phone": personal_info.get("phones", [None])[0],
                "education": json.dumps(extracted_data.get("education", {}), ensure_ascii=False),
                "experience": json.dumps(extracted_data.get("work_experience", {}), ensure_ascii=False),
                "skills": ", ".join([skill.get("name", "") for skill in extracted_data.get("skills", [])]),
                "certifications": json.dumps(extracted_data.get("certifications", []), ensure_ascii=False),
                "ai_content_detection": json.dumps(ai_content_detection, ensure_ascii=False),
                "emotion_detection": json.dumps(emotion_detection, ensure_ascii=False),
                "pii_and_anonymization": json.dumps(pii_and_anonymization, ensure_ascii=False),
                "sentiment_analysis": json.dumps(sentiment_analysis, ensure_ascii=False)
            }
        )

        return Response({
            "message": "Analysis saved successfully",
            "analysis_data": {
                "ai_content_detection": ai_content_detection,
                "emotion_detection": emotion_detection,
                "pii_and_anonymization": pii_and_anonymization,
                "sentiment_analysis": sentiment_analysis
            }
        }, status=status.HTTP_200_OK)

    def ai_content_detection(self, text, headers):
        url = "https://api.edenai.run/v2/text/ai_detection"
        payload = {
            "providers": "originalityai",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def emotion_detection(self, text, headers):
        url = "https://api.edenai.run/v2/text/emotion_detection"
        payload = {
            "providers": "nlpcloud,vernai",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def pii_and_anonymization(self, text, headers):
        url = "https://api.edenai.run/v2/text/anonymization"
        payload = {
            "providers": "emvista",
            "language": "en",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def sentiment_analysis(self, text, headers):
        url = "https://api.edenai.run/v2/text/sentiment_analysis"
        payload = {
            "providers": "google,amazon",
            "language": "en",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}
