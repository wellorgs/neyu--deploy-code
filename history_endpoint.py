import requests

# Replace with your server base URL
base_url = "http://localhost:5000"

# Set parameters for the request
params = {
    "user_id": "testuser123",   # your test user ID
    "botName": "Sage"           # example bot name
}

# Send GET request to /api/history endpoint
response = requests.get(f"{base_url}/api/history", params=params)

# Print HTTP status code
print("Status Code:", response.status_code)

# Print the JSON response
try:
    data = response.json()
    print("Response JSON:", data)
except Exception as e:
    print("Failed to parse JSON:", e)
