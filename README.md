# 🎙️ MeetIQ — AI Meeting Intelligence

Transcribe meetings → Extract action items → Score meeting health → Auto-generate follow-up emails.

Built with **FastAPI + Groq Whisper + Groq LLaMA 3.3 + Vanilla JS**.

## Features

- 🎤 Audio transcription via Groq Whisper (free)
- 📝 AI-generated meeting summaries
- ✅ Automatic action item extraction with owner + deadline + priority
- 📊 Meeting health scoring across 4 dimensions
- 📧 Personalised follow-up email drafts per attendee
- 🖥️ Clean dashboard with live status polling

## Architecture

Audio Upload
↓
FastAPI Background Task
↓
Groq Whisper (transcription)
↓
4 AI Agents (Groq LLaMA 3.3)
├── Summary Agent
├── Action Items Agent
├── Health Score Agent
└── Email Draft Agent
↓
JSON File Storage
↓
Frontend Dashboard (live polling)

## Tech Stack

- **Backend**: FastAPI, Python
- **Transcription**: Groq Whisper (whisper-large-v3)
- **AI Agents**: Groq LLaMA 3.3 70B
- **Storage**: JSON files
- **Frontend**: Vanilla JavaScript, no framework

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your free Groq API key from https://console.groq.com
6. Run backend: `uvicorn day2:app --reload`
7. Open `frontend/index.html` in your browser

## Free API Keys

Get a free Groq API key (no credit card needed):
https://console.groq.com/keys
