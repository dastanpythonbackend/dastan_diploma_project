import requests

resume_id = 1

url = f'http://127.0.0.1:8000/resumes/resume-analyze/{resume_id}/'

token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjg0Njk3LCJpYX'
         'QiOjE3MzIyODEwOTcsImp0aSI6IjBlNzgwOGQ2MjAyODQ4YTM4ZjJkYTM4NjIzNzAzN2NiIiwidXNlcl9pZCI6MX0.EcPxF'
         'TmfpVTUfix-U2mpw8jZbPaOvLDVhd8gemx0gyk')

headers = {
    'Authorization': f'Bearer {token}'
}

try:
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print('Успех:', response.json())
    else:
        print('Не удалось выполнить запрос:', response.status_code, response.text)
except requests.RequestException as e:
    print('Ошибка при выполнении запроса:', e)
