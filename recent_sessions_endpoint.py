import requests

# Replace with your running API base URL
base_url = "http://localhost:5000"

# Specify user_id to test
params = {
    "user_id": "testuser123"  # Replace with your actual user_id
}

# Make GET request to /api/recent_sessions
response = requests.get(f"{base_url}/api/recent_sessions", params=params)

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception:
    print("Response Text:", response.text)
