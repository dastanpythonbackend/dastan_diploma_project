import requests

url = 'http://127.0.0.1:8000/auth/registration-phone_number/'

data = {
  'user': {
    'username': 'johndoe',
    'email': 'johndoe@example.com',
    'password1': 'password123',
    'password2': 'password123'
  },
  'telephone': '+996706476266',
  'role': 'user'
}
response = requests.post(url, json=data)
if response.status_code == 201:
    print('Запрос успешно отправлен.')
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)
