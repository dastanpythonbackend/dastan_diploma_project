import requests

resume_id = 12

url = f"http://127.0.0.1:8000/resumes/resume_analyze/{resume_id}/"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxMzMxMDQ3LCJpYXQiOjE3MzEzMjc0NDcsImp0aSI6IjQ3OTViZDEyMzM3YTRjNzQ4Mzc3NDZmOTZiMDMxMDEzIiwidXNlcl9pZCI6MX0.eSdwGjajB5xpyZVpt6vaFNoAIp52BDNQWcPcUisRU1o"

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
