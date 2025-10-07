import os
import json
from dotenv import load_dotenv
import ruamel.yaml

# Load .env
load_dotenv()

firebase_json = os.getenv("FIREBASE_KEY_JSON")
if not firebase_json:
    raise Exception("❌ FIREBASE_KEY_JSON not found in .env")

# Parse and escape again to ensure clean formatting
firebase_json_clean = json.dumps(json.loads(firebase_json))  # escapes \n and quotes

# Load and modify app.yaml
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

with open("app.yaml", "r") as f:
    data = yaml.load(f)

if "env_variables" not in data:
    data["env_variables"] = {}

data["env_variables"]["FIREBASE_KEY_JSON"] = firebase_json_clean

# Save updated app.yaml
with open("app.yaml", "w") as f:
    yaml.dump(data, f)

print("✅ FIREBASE_KEY_JSON injected into app.yaml!")
