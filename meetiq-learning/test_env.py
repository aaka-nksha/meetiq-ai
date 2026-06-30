from dotenv import load_dotenv
import os

load_dotenv()

groq_key = os.getenv('GROQ_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

if groq_key:
    print('✅ GROQ_API_KEY found:', groq_key[:10], '...')
else:
    print('❌ GROQ_API_KEY not found')

if gemini_key:
    print('✅ GEMINI_API_KEY found:', gemini_key[:10], '...')
else:
    print('❌ GEMINI_API_KEY not found')