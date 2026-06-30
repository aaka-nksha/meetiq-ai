from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="MeetIQ API", version="1.0.0")

# ── Fake in-memory database for learning ──────────────────────
meetings_db = {}


# ── Data model ────────────────────────────────────────────────
class Meeting(BaseModel):
    title: str
    attendees: List[str] = []


# ── Routes ────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "MeetIQ is running!", "total_meetings": len(meetings_db)}


@app.get("/meetings")
def list_meetings():
    return list(meetings_db.values())


@app.get("/meetings/{meeting_id}")
def get_meeting(meeting_id: str):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meetings_db[meeting_id]


@app.post("/meetings")
def create_meeting(meeting: Meeting):
    import uuid
    meeting_id = str(uuid.uuid4())[:8]
    record = {
        "id": meeting_id,
        "title": meeting.title,
        "attendees": meeting.attendees,
        "status": "created"
    }
    meetings_db[meeting_id] = record
    return record


@app.delete("/meetings/{meeting_id}")
def delete_meeting(meeting_id: str):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    del meetings_db[meeting_id]
    return {"message": f"Meeting {meeting_id} deleted"}


@app.get("/search")
def search_meetings(keyword: str, limit: int = 5):
    results = [
        m for m in meetings_db.values()
        if keyword.lower() in m["title"].lower()
    ]
    return results[:limit]