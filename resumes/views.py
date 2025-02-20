import requests
import json

from rest_framework import permissions, generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from django.shortcuts import get_object_or_404


class ResumeCreateAPIView(CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('Пользователь должен быть аутентифицирован, чтобы загрузить резюме.')

        resume = serializer.save(user=self.request.user)
        self.analyze_resume(resume)

    def analyze_resume(self, resume):
        print('Началя анализ резюме.')
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1'
                             'MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0z'
                             'isTPYjCadMSSv7tGc983GrVTNWyw'
        }
        url = 'https://api.edenai.run/v2/ocr/resume_parser'
        json_payload = {
            'providers': 'openai',
        }

        try:
            with open(resume.file.path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, data=json_payload, headers=headers, files=files)

            if response.status_code == 200:
                result = response.json()
                resume.description = result
                resume.analyzed = True
                resume.save()
                print('Резюме успешно проанализировано и сохранено.')
            else:
                print(f'Ошибка при анализе резюме: {response.status_code} - {response.text}')
        except Exception as e:
            print(f'Исключение при анализе резюме: {e}')


class ResumeListAPIView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.AllowAny]


class ResumeDetailView(generics.RetrieveAPIView):
    queryset = ResumeAnalysis.objects.all()
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [permissions.AllowAny]


class ResumeAnalysisAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, resume_id):
        resume = get_object_or_404(Resume, id=resume_id)
        description_data = resume.description
        if not description_data:
            return Response({'error': 'Данные описания пусты'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            extracted_data = description_data.get('openai', {}).get('extracted_data', {})
            personal_info = extracted_data.get('personal_infos', {})
            text_for_analysis = f'{personal_info.get('self_summary', '')} {personal_info.get('objective', '')}'
            if not text_for_analysis.strip():
                text_for_analysis = ' '.join([entry.get('description', '') for entry in
                                              extracted_data.get('work_experience', {}).get('entries', [])])
        except Exception as e:
            return Response({'error': f'Не удалось извлечь текст для анализа: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00O'
                             'TY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadM'
                             'SSv7tGc983GrVTNWyw'
        }

        ai_content_detection = self.ai_content_detection(text_for_analysis, headers)
        emotion_detection = self.emotion_detection(text_for_analysis, headers)
        pii_and_anonymization = self.pii_and_anonymization(text_for_analysis, headers)
        sentiment_analysis = self.sentiment_analysis(text_for_analysis, headers)

        analysis, created = ResumeAnalysis.objects.update_or_create(
            resume=resume,
            defaults={
                'name': personal_info.get('name', {}).get('raw_name'),
                'email': personal_info.get('mails', [None])[0],
                'phone': personal_info.get('phones', [None])[0],
                'education': json.dumps(extracted_data.get('education', {}), ensure_ascii=False),
                'experience': json.dumps(extracted_data.get('work_experience', {}), ensure_ascii=False),
                'skills': ', '.join([skill.get('name', '') for skill in extracted_data.get('skills', [])]),
                'certifications': json.dumps(extracted_data.get('certifications', []), ensure_ascii=False),
                'ai_content_detection': json.dumps(ai_content_detection, ensure_ascii=False),
                'emotion_detection': json.dumps(emotion_detection, ensure_ascii=False),
                'pii_and_anonymization': json.dumps(pii_and_anonymization, ensure_ascii=False),
                'sentiment_analysis': json.dumps(sentiment_analysis, ensure_ascii=False)
            }
        )

        return Response({
            'message': 'Анализ успешно сохранён',
            'analysis_data': {
                'ai_content_detection': ai_content_detection,
                'emotion_detection': emotion_detection,
                'pii_and_anonymization': pii_and_anonymization,
                'sentiment_analysis': sentiment_analysis
            }
        }, status=status.HTTP_200_OK)

    def ai_content_detection(self, text, headers):
        url = 'https://api.edenai.run/v2/text/ai_detection'
        payload = {
            'providers': 'originalityai',
            'text': text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {'error': response.text}

    def emotion_detection(self, text, headers):
        url = 'https://api.edenai.run/v2/text/emotion_detection'
        payload = {
            'providers': 'nlpcloud,vernai',
            'text': text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {'error': response.text}

    def pii_and_anonymization(self, text, headers):
        url = 'https://api.edenai.run/v2/text/anonymization'
        payload = {
            'providers': 'emvista',
            'language': 'en',
            'text': text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {'error': response.text}

    def sentiment_analysis(self, text, headers):
        url = 'https://api.edenai.run/v2/text/sentiment_analysis'
        payload = {
            'providers': 'google,amazon',
            'language': 'en',
            'text': text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {'error': response.text}


class FilteredResumeListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, resume_id):
        resume_analysis = get_object_or_404(ResumeAnalysis, resume_id=resume_id)

        response_data = {
            'name': resume_analysis.name,
            'email': resume_analysis.email,
            'phone': resume_analysis.phone,
            'education': json.loads(resume_analysis.education),
            'experience': json.loads(resume_analysis.experience),
            'skills': resume_analysis.skills,
            'certifications': resume_analysis.certifications,
            'recommendations': resume_analysis.recommendations,
            'ai_content_detection': json.loads(resume_analysis.ai_content_detection),
            'emotion_detection': json.loads(resume_analysis.emotion_detection),
            'pii_and_anonymization': json.loads(resume_analysis.pii_and_anonymization),
            'sentiment_analysis': json.loads(resume_analysis.sentiment_analysis),
        }

        response_data = self.clean_data(response_data)

        for field in ['education', 'experience', 'ai_content_detection', 'emotion_detection', 'pii_and_anonymization',
                      'sentiment_analysis']:
            if field in response_data and isinstance(response_data[field], str):
                try:
                    response_data[field] = json.loads(response_data[field])
                except json.JSONDecodeError:
                    pass

        return Response(response_data)

    def clean_data(self, data):
        if isinstance(data, dict):
            return {
                key: self.clean_data(value)
                for key, value in data.items()
                if value not in [None, '', {}, []]
            }
        elif isinstance(data, list):
            return [self.clean_data(item) for item in data if item not in [None, '', {}, []]]
        else:
            return data
