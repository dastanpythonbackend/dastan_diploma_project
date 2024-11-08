import requests
url = 'http://127.0.0.1:8000/auth/'
data = {
    "username": "asdsads",
    "email": "sadsad@gmail.com",
    "password": "sadasdsa",
    "profile": {
        "role": "asdasd"
    }
}
response = requests.post(url, json=data)
if response.status_code == 201:
    print('Запрос успешно отправлен.')
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)
