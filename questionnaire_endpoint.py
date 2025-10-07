import requests

# URL of the API endpoint
url = "http://localhost:5000/api/start_questionnaire"

# JSON data payload
payload = {
    "topic": "anxiety",
    "user_id": "testuser123"
}

# Send POST request with JSON body
response = requests.post(url, json=payload)

# Print status code and response JSON
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
