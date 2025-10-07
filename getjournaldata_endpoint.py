import requests

base_url = "http://localhost:5000"

# Replace with actual uid and timestamp (ISO8601 format)
params = {
    "uid": "testuser123",
    "timestamp": "2025-09-16T00:00:00Z"
}

response = requests.get(f"{base_url}/getjournaldata", params=params)

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception:
    print("Response Text:", response.text)
