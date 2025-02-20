import requests

url = 'http://127.0.0.1:8000/api/token/refresh/'

data = {
    'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjM3M'
               'TE2NSwiaWF0IjoxNzMyMjg0NzY1LCJqdGkiOiIzZjQ1MWRiODAxZmU0YjNkYTE4YTIyZGQ1ZTBhMmFhOSIsInV'
               'zZXJfaWQiOjF9.leVxYIXbYPYOVlt7CcdDxYFI44PuzJ1jUen2F-Ua7-M'
}

response = requests.post(url, json=data)
if response.status_code == 200:
    print('Запрос успешно отправлен.', response.json())
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)