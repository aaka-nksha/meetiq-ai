from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from transcription import transcribe_audio
from agents import run_meeting_agents
from storage import save_meeting, get_meeting, list_meetings
import uuid

app = FastAPI(title="MeetIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".webm"}


def process_meeting(meeting_id: str, file_path: str, title: str, attendees: list):
    """Full AI pipeline — runs in background."""
    try:
        meeting = get_meeting(meeting_id)

        # Stage 1: Transcribe
        meeting["status"] = "transcribing"
        save_meeting(meeting_id, meeting)
        meeting["transcript"] = transcribe_audio(file_path)
        save_meeting(meeting_id, meeting)

        # Stage 2: Run all 4 agents
        meeting["status"] = "analysing"
        save_meeting(meeting_id, meeting)
        results = run_meeting_agents(meeting["transcript"], title, attendees)

        # Stage 3: Save results
        meeting.update(results)
        meeting["status"] = "done"
        save_meeting(meeting_id, meeting)

    except Exception as e:
        meeting = get_meeting(meeting_id) or {}
        meeting["status"] = "error"
        meeting["error"] = str(e)
        save_meeting(meeting_id, meeting)
        print(f"❌ Pipeline error: {e}")


@app.post("/upload-meeting")
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form("Meeting"),
    attendees: str = Form("")
):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_TYPES:
        raise HTTPException(400, "Audio files only")

    meeting_id = str(uuid.uuid4())[:8]
    save_path = UPLOAD_DIR / f"{meeting_id}{suffix}"
    with open(save_path, "wb") as f:
        f.write(await file.read())

    attendee_list = [e.strip() for e in attendees.split(",") if e.strip()]

    meeting = {
        "id": meeting_id,
        "title": title,
        "attendees": attendee_list,
        "status": "queued",
        "transcript": None,
        "summary": None,
        "action_items": [],
        "health_score": None,
        "health_breakdown": None,
        "email_drafts": []
    }
    save_meeting(meeting_id, meeting)

    background_tasks.add_task(
        process_meeting,
        meeting_id,
        str(save_path),
        title,
        attendee_list
    )

    return {
        "meeting_id": meeting_id,
        "status": "queued",
        "message": "Processing started!"
    }


@app.get("/meeting/{meeting_id}")
def get_meeting_endpoint(meeting_id: str):
    meeting = get_meeting(meeting_id)
    if not meeting:
        raise HTTPException(404, "Meeting not found")
    return meeting


@app.get("/meetings")
def list_meetings_endpoint():
    return list_meetings()