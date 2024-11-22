import requests  # Импортируем библиотеку для работы с HTTP-запросами

# Идентификатор резюме, который будем анализировать
resume_id = 1

# Формируем URL для запроса, включая идентификатор резюме в пути
url = f"http://127.0.0.1:8000/resumes/resume_analyze/{resume_id}/"

# JWT токен для авторизации. Используется для аутентификации пользователя на сервере
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjg0Njk3LCJpYXQiOjE3MzIyODEwOTcsImp0aSI6IjBlNzgwOGQ2MjAyODQ4YTM4ZjJkYTM4NjIzNzAzN2NiIiwidXNlcl9pZCI6MX0.EcPxFTmfpVTUfix-U2mpw8jZbPaOvLDVhd8gemx0gyk"

# Заголовки запроса, включающие авторизационный токен для аутентификации
headers = {
    "Authorization": f"Bearer {token}"  # Токен передается через заголовок Authorization
}

# Попытка отправить POST-запрос к серверу
try:
    response = requests.post(url, headers=headers)  # Отправка запроса с токеном в заголовках

    if response.status_code == 200:
        # Если статус ответа 200 (успешно), выводим данные, полученные от сервера
        print("Успех:", response.json())
    else:
        # В случае ошибки выводим код статуса и текст ошибки
        print("Не удалось выполнить запрос:", response.status_code, response.text)
except requests.RequestException as e:
    # Если произошла ошибка в процессе запроса (например, ошибка сети), выводим сообщение об ошибке
    print("Ошибка при выполнении запроса:", e)
