# Импортируем библиотеку requests для работы с HTTP-запросами
import requests

# Указываем URL для API, с которым будем работать
url = "http://127.0.0.1:8000/auth/registration_phone_number/"

# Создаем данные для отправки в запросе (например, для регистрации по номеру телефона)
data = {
  "user": {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password1": "password123",
    "password2": "password123"
  },
  "telephone": "+996706476266",
  "role": "user"
}

# Отправляем POST-запрос на сервер с указанным URL и данными в формате JSON
response = requests.post(url, json=data)

# Проверяем статус код ответа, чтобы понять, успешен ли запрос
if response.status_code == 201:
    # Если код ответа 201 (создание ресурса), выводим сообщение об успехе
    print('Запрос успешно отправлен.')
else:
    # Если код ответа не 201, выводим ошибку и код ответа от сервера
    print('Ошибка при отправке запроса:', response.status_code, response.text)
