import requests

# Replace with your API server URL and port
base_url = "http://localhost:5000"

# Make GET request to /journallist
response = requests.get(f"{base_url}/journallist")

# Print response status code and the result JSON (or text if not JSON)
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception:
    print("Response Text:", response.text)
