import requests

url = "http://127.0.0.1:8000/resumes/resume_create/"

# JWT токен
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxMzMxMDQ3LCJpYXQiOjE3MzEzMjc0NDcsImp0aSI6IjQ3OTViZDEyMzM3YTRjNzQ4Mzc3NDZmOTZiMDMxMDEzIiwidXNlcl9pZCI6MX0.eSdwGjajB5xpyZVpt6vaFNoAIp52BDNQWcPcUisRU1o"

# Заголовки с токеном авторизации
headers = {
    "Authorization": f"Bearer {token}"
}

file_path = "Мырсалиев_Дастан_Резюме (1).pdf"

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
