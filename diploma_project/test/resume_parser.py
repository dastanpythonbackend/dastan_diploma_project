import requests

url = "http://127.0.0.1:8000/resumes/resumes/create/"

# JWT токен
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwOTAzMTc4LCJpYXQiOjE3MzA4OTk1NzgsImp0aSI6ImVlZDUwM2RkYWE5MDQ5Njg4YWJiMjBkZTU0ZDYxOGNkIiwidXNlcl9pZCI6MX0.0OdOxH9OhA4Bz4rmu0YwmNyetIGL89KRmsODbFzMhHM"

# Заголовки с токеном авторизации
headers = {
    "Authorization": f"Bearer {token}"
}

file_path = "Мырсалиев_Дастан_Резюме.pdf"

data = {
    "title": "My Resume Title",

}

# Открываем файл и отправляем POST-запрос
with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, headers=headers, data=data, files=files)

# Обрабатываем ответ
if response.status_code == 201:
    print("Resume uploaded successfully.")
    print("Response data:", response.json())
else:
    print(f"Failed to upload resume. Status code: {response.status_code}")
    print("Error response:", response.text)
