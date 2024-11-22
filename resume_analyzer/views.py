import requests
import json
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer


# Представление для создания резюме
class ResumeCreateAPIView(CreateAPIView):
    queryset = Resume.objects.all()  # Все резюме в базе данных
    serializer_class = ResumeSerializer  # Используемый сериализатор для валидации данных
    permission_classes = [permissions.IsAuthenticated]  # Только для аутентифицированных пользователей

    def perform_create(self, serializer):
        """
        Этот метод вызывается при сохранении нового резюме.
        Сначала проверяется, аутентифицирован ли пользователь.
        Если пользователь аутентифицирован, то резюме созхраняется, и выполняется его анализ.
        """
        if self.request.user.is_anonymous:
            raise NotAuthenticated("Пользователь должен быть аутентифицирован, чтобы загрузить резюме.")

        # Сохраняем резюме, привязываем его к текущему пользователю
        resume = serializer.save(user=self.request.user)
        # После сохраняем резюме, начиная его анализ
        self.analyze_resume(resume)

    def analyze_resume(self, resume):
        """
         Метод для анализа загруженного резюме с использованием внешнего API.
         Загружает резюме и отправляет его в API для анализа.
        """
        print("Началя анализ резюме.")
        # Заголовки для авторизации с использованием токена API
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTRiMDQ0NTktZjQ1MS00OTY4LTlhM2UtYjhiNmI4ZTJhMDcwIiwidHlwZSI6ImFwaV90b2tlbiJ9.ukZ22dwwefVnF0zisTPYjCadMSSv7tGc983GrVTNWyw"
        }
        url = "https://api.edenai.run/v2/ocr/resume_parser"
        json_payload = {
            "providers": "openai",  # Указываем поставщика для обработки резюме
        }

        try:
            # Открываем файл резюме и отправляем его в API для анализа
            with open(resume.file.path, "rb") as f:
                files = {"file": f}
                response = requests.post(url, data=json_payload, headers=headers, files=files)

            # Если запрос успешен, сохраняем результаты анализа
            if response.status_code == 200:
                result = response.json()
                resume.description = result  # Сохраняем результаты анализа в поле description
                resume.analyzed = True  # Помечаем резюме как проанализированное
                resume.save()
                print("Резюме успешно проанализировано и сохранено.")
            else:
                print(f"Ошибка при анализе резюме: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Исключение при анализе резюме: {e}")


# Представление для получения списка всех резюме
class ResumeListAPIView(generics.ListAPIView):
    queryset = Resume.objects.all()  # Получаем все резюме из базы данных
    serializer_class = ResumeSerializer  # Сериализатор для преобразования в формат JSON
    permission_classes = [permissions.AllowAny]  # Доступно для всех пользователей


# Представление для получения данных об одном резюме
class ResumeDetailView(generics.RetrieveAPIView):
    queryset = ResumeAnalysis.objects.all()  # Получаем данные анализа резюме
    serializer_class = ResumeAnalysisSerializer  # Сериализатор для отображения данных анализа
    permission_classes = [permissions.AllowAny]  # Доступно для всех пользователей


# Представление для выполнения анализа резюме с использованием внешних API
class ResumeAnalysisAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Доступно для всех пользователей

    def post(self, request, resume_id):
        # Получаем резюме по ID
        resume = get_object_or_404(Resume, id=resume_id)

        # Извлечение данных из поля description, которое содержит результат анализа резюме
        description_data = resume.description
        if not description_data:
            return Response({"error": "Данные описания пусты"}, status=status.HTTP_400_BAD_REQUEST)

        # Пример извлечения нужного текста для анализа
        try:
            extracted_data = description_data.get("openai", {}).get("extracted_data", {})
            personal_info = extracted_data.get("personal_infos", {})
            text_for_analysis = f"{personal_info.get('self_summary', '')} {personal_info.get('objective', '')}"
            if not text_for_analysis.strip():
                text_for_analysis = " ".join([entry.get("description", "") for entry in
                                              extracted_data.get("work_experience", {}).get("entries", [])])
        except Exception as e:
            return Response({"error": f"Не удалось извлечь текст для анализа: {str(e)}"},
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
            resume=resume,  # Связываем анализ с конкретным резюме
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
            "message": "Анализ успешно сохранён",
            "analysis_data": {
                "ai_content_detection": ai_content_detection,
                "emotion_detection": emotion_detection,
                "pii_and_anonymization": pii_and_anonymization,
                "sentiment_analysis": sentiment_analysis
            }
        }, status=status.HTTP_200_OK)

    # Методы для выполнения различных видов анализа текста

    def ai_content_detection(self, text, headers):
        """Метод для определения оригинальности текста с помощью ИИ"""
        url = "https://api.edenai.run/v2/text/ai_detection"
        payload = {
            "providers": "originalityai",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def emotion_detection(self, text, headers):
        """Метод для распознавания эмоций в тексте"""
        url = "https://api.edenai.run/v2/text/emotion_detection"
        payload = {
            "providers": "nlpcloud,vernai",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def pii_and_anonymization(self, text, headers):
        """Метод для анонимизации персональных данных"""
        url = "https://api.edenai.run/v2/text/anonymization"
        payload = {
            "providers": "emvista",
            "language": "en",
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def sentiment_analysis(self, text, headers):
        """
        Метод для выполнения анализа настроений в тексте с использованием внешнего API.
        Используются провайдеры Google и Amazon для анализа настроений.
        """
        url = "https://api.edenai.run/v2/text/sentiment_analysis"
        payload = {
            "providers": "google,amazon",  # Указываем провайдеров для анализа
            "language": "en",  # Язык текста
            "text": text  # Текст, который необходимо проанализировать
        }
        # Отправляем запрос к API
        response = requests.post(url, json=payload, headers=headers)

        # Возвращаем результат в формате JSON, если запрос успешен, или сообщение об ошибке
        return response.json() if response.status_code == 200 else {"error": response.text}


# Представление для фильтрации данных анализа резюме
class FilteredResumeListView(APIView):
    permission_classes = [permissions.AllowAny]  # Доступно для всех пользователей

    def get(self, request, resume_id):
        """
        Метод для получения отфильтрованных данных анализа резюме по его ID.
        Фильтруются пустые значения, такие как None, пустые строки и пустые объекты/списки.
        """
        # Получаем объект анализа резюме по ID
        resume_analysis = get_object_or_404(ResumeAnalysis, resume_id=resume_id)

        # Собираем данные для ответа, включая все необходимые поля из объекта анализа
        response_data = {
            "name": resume_analysis.name,
            "email": resume_analysis.email,
            "phone": resume_analysis.phone,
            "education": json.loads(resume_analysis.education),  # Преобразуем строку в JSON
            "experience": json.loads(resume_analysis.experience),   # Преобразуем строку в JSON
            "skills": resume_analysis.skills,
            "certifications": resume_analysis.certifications,
            "recommendations": resume_analysis.recommendations,
            "ai_content_detection": json.loads(resume_analysis.ai_content_detection),  # Преобразуем строку в JSON
            "emotion_detection": json.loads(resume_analysis.emotion_detection),  # Преобразуем строку в JSON
            "pii_and_anonymization": json.loads(resume_analysis.pii_and_anonymization),  # Преобразуем строку в JSON
            "sentiment_analysis": json.loads(resume_analysis.sentiment_analysis),  # Преобразуем строку в JSON
        }

        # Фильтруем данные, удаляя поля с None, пустыми строками или пустыми объектами
        response_data = self.clean_data(response_data)

        # Преобразуем JSON-строки в объекты, если они существуют
        for field in ["education", "experience", "ai_content_detection", "emotion_detection", "pii_and_anonymization",
                      "sentiment_analysis"]:
            if field in response_data and isinstance(response_data[field], str):
                try:
                    response_data[field] = json.loads(response_data[field])  # Преобразуем строку в объект
                except json.JSONDecodeError:
                    pass  # В случае ошибки пропускаем преобразование

        # Возвращаем отфильтрованные данные
        return Response(response_data)

    def clean_data(self, data):
        """
        Рекурсивная очистка данных от пустых значений, таких как None, пустые строки, пустые объекты и пустые списки.
        """
        if isinstance(data, dict):
            # Для словаря удаляем ключи с None, пустыми строками или пустыми объектами
            return {
                key: self.clean_data(value)  # Рекурсивно очищаем значения
                for key, value in data.items()
                if value not in [None, "", {}, []]  # Убираем пустые или пустые объекты
            }
        elif isinstance(data, list):
            # Для списка удаляем пустые элементы
            return [self.clean_data(item) for item in data if item not in [None, "", {}, []]]
        else:
            # Для остальных типов данных возвращаем их без изменений
            return data
