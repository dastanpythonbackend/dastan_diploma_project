import requests  # Импортируем библиотеку для выполнения HTTP-запросов

# URL для обновления токена
url = "http://127.0.0.1:8000/api/token/refresh/"

# Данные для обновления токена
data = {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjM3MTE2NSwiaWF0IjoxNzMyMjg0NzY1LCJqdGkiOiIzZjQ1MWRiODAxZmU0YjNkYTE4YTIyZGQ1ZTBhMmFhOSIsInVzZXJfaWQiOjF9.leVxYIXbYPYOVlt7CcdDxYFI44PuzJ1jUen2F-Ua7-M"
}

# Отправляем POST-запрос на сервер для получения токена
response = requests.post(url, json=data)

# Проверяем статус ответа от сервера
if response.status_code == 200:
    # Если запрос успешен (код 200), выводим сообщение и данные ответа в формате JSON
    print('Запрос успешно отправлен.', response.json())
else:
    # Если произошла ошибка (статус не 200), выводим сообщение об ошибке с кодом ответа и текстом
    print('Ошибка при отправке запроса:', response.status_code, response.text)