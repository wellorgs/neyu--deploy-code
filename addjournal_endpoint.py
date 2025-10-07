import requests
from firebase_admin import storage

# Replace with your server URL
url = "http://localhost:5000/addjournal"

# Required form data
data = {
    'uid': 'testuser123',
    'name': 'Daily Reflection',
    'message': 'Today I felt calm and relaxed.'
}


try:
    

    # If testing without image, use below instead:
    response = requests.post(url, data=data)

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

except Exception as e:
    print("Error during request:", e)
