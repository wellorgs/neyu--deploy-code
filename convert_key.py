import json

# Load the firebase key from the JSON file
with open('firebase-key.json') as f:
    data = json.load(f)

# Dump as a single-line JSON string, with escaped characters
escaped_json = json.dumps(data)

# Write to .env file
with open('.env', 'a') as env_file:
    env_file.write(f'FIREBASE_KEY_JSON={escaped_json}\n')

print("✅ Escaped FIREBASE_KEY_JSON added to .env")
