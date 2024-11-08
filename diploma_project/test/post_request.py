import requests

# Задайте URL вашего API
url = 'http://127.0.0.1:8000/resumes/'  # Замените на актуальный URL

# Подготовьте данные для запроса
data = {
    'file': '8.pdf',  # Укажите путь к вашему файлу
    'title': 'My Resume',
    'description': 'This is my resume.',
}

# Если требуется аутентификация, укажите заголовок с токеном
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4OTE3MDUxLCJpYXQiOjE3Mjg5MTM0NTEsImp0aSI6IjFlMTY4NTM2MjdlMjRiYTU5MTUyYThmNTNmYTY0M2ZiIiwidXNlcl9pZCI6MX0.Pw8RXQMKqGbDXg_cD9bGYNp6N0cup6Zor9PLKNxJGFE',  # Замените YOUR_TOKEN на актуальный токен
}

# Выполните POST-запрос
with open(data['file'], 'rb') as f:
    response = requests.post(url, headers=headers, files={'file': f}, json=data)

# Проверьте статус-код ответа
if response.status_code == 201:  # Успешное создание ресурса
    print('Резюме успешно загружено:', response.json())
else:
    print('Ошибка при загрузке резюме:', response.status_code, response.text)
