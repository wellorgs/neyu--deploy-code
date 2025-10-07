import requests

# Replace with your server URL and port if different
base_url = "http://localhost:5000"

# Parameters to send in query string
params = {
    "user_id": "testuser123"  # Replace with actual user_id you want to test
}

# Make the GET request
response = requests.get(f"{base_url}/api/last_active_session", params=params)

# Print response status code and JSON data (or text if JSON fails)
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception:
    print("Response Text:", response.text)
