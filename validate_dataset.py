import json

with open(r"C:\Users\MY PC\Downloads\AI-therapy-static-model-withjson\AI-therapy-static-model-withjson\merged_bots_clean.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

bots = data['bots']
first_bot = bots[0]

conversations = first_bot['conversations']

print(type(conversations))  # should be list

message_1194 = conversations[1194]
print(message_1194)
