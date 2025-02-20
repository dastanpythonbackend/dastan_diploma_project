import requests

url = 'http://127.0.0.1:8000/resumes/resume_create/'

token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjg0Njk3LC'
         'JpYXQiOjE3MzIyODEwOTcsImp0aSI6IjBlNzgwOGQ2MjAyODQ4YTM4ZjJkYTM4NjIzNzAzN2NiIiwidXNlcl9pZCI6M'
         'X0.EcPxFTmfpVTUfix-U2mpw8jZbPaOvLDVhd8gemx0gyk')

headers = {
    'Authorization': f'Bearer {token}'
}

file_path = 'Мырсалиев_Дастан_Резюме (1).pdf'

data = {
    'title': 'Заголовок моего резюме',
}

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 201:
    print('Резюме успешно загружено.')
    print('Ответ от сервера:', response.json())
else:
    print(f'Не удалось загрузить резюме. Код статуса: {response.status_code}')
    print('Ошибка в ответе:', response.text)
