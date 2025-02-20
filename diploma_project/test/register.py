import requests

url = 'http://127.0.0.1:8000/auth/register/'

data = {
    'username': 'dastan',
    'email': 'dastan@gmail.com',
    'password1': 'dastan123456',
    'password2': 'dastan123456'
}
response = requests.post(url, json=data)
if response.status_code == 201:
    print('Запрос успешно отправлен.')
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)
