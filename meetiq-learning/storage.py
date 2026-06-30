import json
from pathlib import Path
from datetime import datetime

DB_DIR = Path("meetings_db")
DB_DIR.mkdir(exist_ok=True)


def save_meeting(meeting_id: str, data: dict):
    """Save or update a meeting record."""
    if "created_at" not in data:
        data["created_at"] = datetime.now().isoformat()
    data["updated_at"] = datetime.now().isoformat()

    path = DB_DIR / f"{meeting_id}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  💾 Saved meeting {meeting_id} — status: {data.get('status')}")


def get_meeting(meeting_id: str):
    """Get a single meeting by ID."""
    path = DB_DIR / f"{meeting_id}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def list_meetings():
    """List all meetings sorted by most recent first."""
    meetings = []

    for path in sorted(
        DB_DIR.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    ):
        try:
            with open(path) as f:
                data = json.load(f)

            # Debug print so you can see what's being loaded
            print(f"  📂 Loading: {path.name} — title: {data.get('title')} — status: {data.get('status')}")

            meetings.append({
                "id":                 data.get("id", path.stem),
                "title":              data.get("title") or "Untitled Meeting",
                "status":             data.get("status", "unknown"),
                "health_score":       data.get("health_score"),
                "action_items_count": len(data.get("action_items", [])),
                "attendees":          data.get("attendees", []),
                "created_at":         data.get("created_at"),
            })

        except Exception as e:
            print(f"  ⚠️  Could not read {path.name}: {e}")

    return meetings


def delete_meeting(meeting_id: str) -> bool:
    """Delete a meeting record."""
    path = DB_DIR / f"{meeting_id}.json"
    if path.exists():
        path.unlink()
        print(f"  🗑️  Deleted meeting {meeting_id}")
        return True
    return False