from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

response = client.chat.completions.create(
    model='llama-3.3-70b-versatile',   # free model on Groq
    messages=[
        {'role': 'user', 'content': 'Say hello in one sentence'}
    ]
)

print('✅ Groq working!')
print('Response:', response.choices[0].message.content)