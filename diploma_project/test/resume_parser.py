import requests  # Импортируем библиотеку для работы с HTTP-запросами

# URL для API, куда будем отправлять запрос
url = "http://127.0.0.1:8000/resumes/resume_create/"

# JWT токен для авторизации, необходимый для доступа к API
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjg0Njk3LCJpYXQiOjE3MzIyODEwOTcsImp0aSI6IjBlNzgwOGQ2MjAyODQ4YTM4ZjJkYTM4NjIzNzAzN2NiIiwidXNlcl9pZCI6MX0.EcPxFTmfpVTUfix-U2mpw8jZbPaOvLDVhd8gemx0gyk"

# Заголовки для запроса, включая токен авторизации
headers = {
    "Authorization": f"Bearer {token}"  # Добавляем токен в заголовок для аутентификации
}

# Путь к файлу, который будет отправлен
file_path = "Мырсалиев_Дастан_Резюме (1).pdf"

# Данные для отправки с запросом, например, заголовок резюме
data = {
    "title": "Заголовок моего резюме",  # Заголовок резюме
}

# Открываем файл в режиме бинарного чтения (rb) и отправляем POST-запрос
with open(file_path, "rb") as f:
    files = {"file": f}  # Открытый файл передаем в поле "file"
    # Отправляем POST-запрос на сервер с заголовками, данными и файлом
    response = requests.post(url, headers=headers, data=data, files=files)

# Проверяем ответ от сервера
if response.status_code == 201:
    # Если код ответа 201 (ресурс успешно создан), выводим сообщение об успехе
    print("Резюме успешно загружено.")
    print("Ответ от сервера:", response.json())  # Выводим данные, полученные от сервера
else:
    # В случае ошибки выводим код статуса и сообщение об ошибке
    print(f"Не удалось загрузить резюме. Код статуса: {response.status_code}")
    print("Ошибка в ответе:", response.text)
