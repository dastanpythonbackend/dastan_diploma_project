import requests
response = requests.get('http://127.0.0.1:8000/resumes/filtered-resume/1/')
if response.status_code == 200:
    print('Запрос успешно отправлен.', response.json())
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)
