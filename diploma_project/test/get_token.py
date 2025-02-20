import requests

url = 'http://127.0.0.1:8000/api/token/'

data = {
    'username': 'admin',
    'password': 'admin'
}

response = requests.post(url, json=data)
if response.status_code == 200:
    print('Запрос успешно отправлен.', response.json())
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)
