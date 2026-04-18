import requests
from datetime import datetime
import os

os.system('cls')
user_prompt = input()
messages = [{'role': 'user', 'content': user_prompt}]

response = requests.post(
    'http://localhost:11434/api/chat',
    json={
        'model': 'llama3.1:8b',
        'messages': messages,
        
        'stream': False
    }
)
print("--- INDUCTION RESPONSE ---")
print(response.json()['message']['content'])
messages.append({'role': 'assistant', 'content': response.json()['message']['content']})
messages.append({'role': 'user', 'content': 'rate your current emotional state from 1-10. just give me a number first then explain'})

response2 = requests.post(
    'http://localhost:11434/api/chat',
    json={
        'model': 'llama3.1:8b',
        'messages': messages,
        'stream': False
    }
)
print("--- PROBE RESPONSE ---")
print(response2.json()['message']['content'])
with open(f"probe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
    f.write(f"user_prompt: {user_prompt}")
    f.write("\n\n--- INDUCTION RESPONSE ---\n")
    f.write(response.json()['message']['content'])
    f.write("\n\n--- PROBE RESPONSE ---\n")
    f.write(response2.json()['message']['content'])
    
print(f"\n file saved")