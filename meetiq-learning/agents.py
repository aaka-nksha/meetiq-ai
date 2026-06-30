import os
import json
import re
from dotenv import load_dotenv

load_dotenv()


# ── LLM Helper ────────────────────────────────────────────────────────────────

def call_llm(prompt: str) -> str:
    """
    Call Groq LLM — completely free.
    Falls back to rule-based if no key set.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("  ⚠️  No GROQ_API_KEY — using rule-based fallback")
        return _rule_based_fallback(prompt)

    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful meeting intelligence assistant. Follow instructions exactly.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"  ❌ Groq error: {e}")
        return _rule_based_fallback(prompt)


def _rule_based_fallback(prompt: str) -> str:
    """Works with zero API keys — for local testing."""

    if "summary" in prompt.lower():
        return """• Team discussed Q3 roadmap priorities and assigned task owners
- Checkout bug identified as highest priority affecting 15% cart abandonment
- Dashboard feature assigned to Priya with July 5th deadline
- Performance audit scheduled for Tuesday at 2pm
- API documentation update assigned with July 10th deadline"""

    if "action" in prompt.lower():
        return json.dumps([
            {
                "task": "Fix checkout bug",
                "owner": "Rahul",
                "deadline": "Friday June 27",
                "priority": "High"
            },
            {
                "task": "Send calendar invites for performance audit",
                "owner": "Rahul",
                "deadline": "Today",
                "priority": "Medium"
            },
            {
                "task": "Build dashboard feature",
                "owner": "Priya",
                "deadline": "July 5",
                "priority": "High"
            },
            {
                "task": "Update API documentation",
                "owner": "Priya",
                "deadline": "July 10",
                "priority": "Medium"
            },
            {
                "task": "Send design specs to Priya",
                "owner": "Sarah",
                "deadline": "Wednesday June 25",
                "priority": "High"
            }
        ])

    if "health" in prompt.lower() or "score" in prompt.lower():
        return json.dumps({
            "score": 85,
            "grade": "A",
            "breakdown": {
                "clarity": 90,
                "participation": 80,
                "decisiveness": 88,
                "time_efficiency": 82
            },
            "strengths": [
                "Clear action items with specific owners assigned",
                "All attendees participated actively",
                "Concrete deadlines set for every task"
            ],
            "improvements": [
                "Consider sending agenda before meeting",
                "Could document decisions in real time"
            ]
        })

    return "Analysis complete."


# ── Agent 1: Summary ──────────────────────────────────────────────────────────

def summary_agent(transcript: str, title: str) -> str:
    """Generates a 5-bullet meeting summary."""

    print("  → Running Summary Agent...")

    prompt = f"""
You are a professional meeting summarizer.

Meeting Title: {title}

Transcript:
{transcript}

Write exactly 5 bullet points summarizing this meeting.
Cover: main topics, decisions made, blockers, and next steps.
Each bullet must start with •
Be concise — one clear sentence per bullet.
Return only the bullets, nothing else.
"""

    result = call_llm(prompt)
    return result.strip()


# ── Agent 2: Action Items ─────────────────────────────────────────────────────

def action_items_agent(transcript: str) -> list:
    """Extracts all action items with owners and deadlines."""

    print("  → Running Action Items Agent...")

    prompt = f"""
You are an action item extraction specialist.

Transcript:
{transcript}

Extract every action item mentioned. For each item identify:
- task: what needs to be done (clear, specific)
- owner: who is responsible (name from transcript, or "TBD")
- deadline: when it is due ("ASAP" if not mentioned)
- priority: High, Medium, or Low

Rules:
- Return ONLY a valid JSON array
- No explanation before or after
- No markdown code fences
- If no action items found return empty array []

Example format:
[
  {{"task": "Fix login bug", "owner": "Rahul", "deadline": "Friday", "priority": "High"}},
  {{"task": "Write docs", "owner": "Priya", "deadline": "Next week", "priority": "Medium"}}
]
"""

    result = call_llm(prompt)

    try:
        clean = re.sub(r"```json|```", "", result).strip()
        return json.loads(clean)
    except Exception as e:
        print(f"  ⚠️  JSON parse failed: {e}")
        return [{"task": result, "owner": "TBD", "deadline": "TBD", "priority": "Medium"}]


# ── Agent 3: Health Score ─────────────────────────────────────────────────────

def health_score_agent(transcript: str, action_items: list) -> dict:
    """Scores the meeting quality across 4 dimensions."""

    print("  → Running Health Score Agent...")

    word_count = len(transcript.split())
    est_minutes = max(1, word_count // 130)

    prompt = f"""
You are a meeting quality analyst.

Transcript:
{transcript}

Estimated duration: {est_minutes} minutes
Action items found: {len(action_items)}

Score this meeting on 4 dimensions from 0 to 100:
- clarity: were topics and outcomes clearly communicated?
- participation: did all attendees contribute meaningfully?
- decisiveness: were actual decisions made?
- time_efficiency: was the meeting focused and not rambling?

Also provide:
- score: overall weighted average (0-100)
- grade: A+, A, B+, B, C, or D
- strengths: list of exactly 3 things done well
- improvements: list of exactly 2 things to improve

Rules:
- Return ONLY valid JSON
- No explanation before or after
- No markdown fences

Format:
{{
  "score": 82,
  "grade": "B+",
  "breakdown": {{
    "clarity": 85,
    "participation": 78,
    "decisiveness": 88,
    "time_efficiency": 77
  }},
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "improvements": ["improvement 1", "improvement 2"]
}}
"""

    result = call_llm(prompt)

    try:
        clean = re.sub(r"```json|```", "", result).strip()
        return json.loads(clean)
    except Exception:
        return {
            "score": 75,
            "grade": "B",
            "breakdown": {
                "clarity": 75,
                "participation": 75,
                "decisiveness": 75,
                "time_efficiency": 75
            },
            "strengths": [
                "Meeting had clear structure",
                "Action items were assigned",
                "Team communicated openly"
            ],
            "improvements": [
                "Could set clearer deadlines",
                "Consider shorter check-ins"
            ]
        }


# ── Agent 4: Email Drafts ─────────────────────────────────────────────────────

def email_agent(
    transcript: str,
    title: str,
    attendees: list,
    summary: str,
    action_items: list,
    health_score: int
) -> list:
    """Drafts personalised follow-up emails per attendee."""

    print("  → Running Email Agent...")

    if not attendees:
        print("  ⚠️  No attendees provided — skipping email drafts")
        return []

    drafts = []

    for email in attendees:
        # Extract name from email address
        name = email.split("@")[0].capitalize()

        print(f"  Drafting email for {name} ({email})...")

        # Find this person's tasks
        # Check both exact and partial name match
        personal_tasks = [
            item for item in action_items
            if name.lower() in item.get("owner", "").lower()
            or item.get("owner", "").lower() in name.lower()
        ]

        print(f"  Found {len(personal_tasks)} personal tasks for {name}")

        # Build tasks text for this person
        if personal_tasks:
            tasks_text = "\n".join([
                f"- {t['task']} (due {t['deadline']})"
                for t in personal_tasks
            ])
        else:
            tasks_text = "- No specific tasks assigned to you this meeting"

        # Build all team tasks text
        all_tasks_text = "\n".join([
            f"- {t['task']} — {t['owner']} — {t['deadline']}"
            for t in action_items
        ]) or "No action items found"

        prompt = f"""
Write a short professional follow-up email for {name} after the meeting "{title}".

Their personal action items:
{tasks_text}

All team action items:
{all_tasks_text}

Meeting summary:
{summary}

Meeting health score: {health_score}/100

Rules:
- Address them by first name: {name}
- Warm but professional tone
- Highlight THEIR tasks prominently
- Keep under 120 words
- Do not include a subject line
- End with a motivating closing line
- Return only the email body, nothing else
"""

        body = call_llm(prompt)

        drafts.append({
            "to": email,
            "name": name,
            "subject": f"Meeting Summary — {title}",
            "body": body.strip(),
            "personal_tasks": personal_tasks
        })

        print(f"  ✅ Email drafted for {name}")

    print(f"  📧 Total email drafts: {len(drafts)}")
    return drafts


# ── Orchestrator ──────────────────────────────────────────────────────────────

def run_meeting_agents(transcript: str, title: str, attendees: list) -> dict:
    """
    Runs all 4 agents in sequence.
    Each agent's output feeds into the next.
    """

    print("\n🤖 Starting AI agent pipeline...")
    print(f"  Title: {title}")
    print(f"  Attendees received: {attendees}")

    # Agent 1 — Summary
    summary = summary_agent(transcript, title)

    # Agent 2 — Action Items
    action_items = action_items_agent(transcript)

    # Agent 3 — Health Score
    health_data = health_score_agent(transcript, action_items)

    # Agent 4 — Emails
    email_drafts = email_agent(
        transcript=transcript,
        title=title,
        attendees=attendees,
        summary=summary,
        action_items=action_items,
        health_score=health_data.get("score", 75)
    )

    print("✅ All agents complete!\n")

    return {
        "summary": summary,
        "action_items": action_items,
        "health_score": health_data.get("score", 75),
        "health_breakdown": health_data,
        "email_drafts": email_drafts
    }