import requests

# Set the base URL of your running server
base_url = "http://localhost:5000"

# Define the parameters expected by the endpoint
params = {
    "user_id": "testuser123",
    "botName": "Sage"  # or another bot name like "Jordan", "River", etc.
}

# Make a GET request to /api/session_summary with the params
response = requests.get(f"{base_url}/api/session_summary", params=params)

# Print status code and JSON response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
