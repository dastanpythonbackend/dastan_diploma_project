import requests

resume_id = 11

url = f"http://127.0.0.1:8000/resumes/resumes/{resume_id}/analyze/"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwODk5Njk1LCJpYXQiOjE3MzA4OTYwOTUsImp0aSI6IjVlOWYzNDE5MzE2YjQ5Mjk5YThiNGVhZWQxYjFmMDBmIiwidXNlcl9pZCI6MX0._9wYTxOJJueGEtUJ_4oEYWJWcYApVu8Ai5Xai23K5Ns"

headers = {
    "Authorization": f"Bearer {token}"
}

try:
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.status_code, response.text)
except requests.RequestException as e:
    print("Request failed:", e)
