import os
from dotenv import load_dotenv

load_dotenv()


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio using Groq Whisper — free.
    Falls back to mock transcript if no API key.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("⚠️  No GROQ_API_KEY found — using mock transcript")
        return _mock_transcript()

    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        print(f"  Sending {file_path} to Groq Whisper...")

        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                response_format="text"
            )

        print(f"  ✅ Transcription done! ({len(transcription)} characters)")
        return transcription

    except Exception as e:
        print(f"  ❌ Groq Whisper error: {e}")
        print("  Falling back to mock transcript")
        return _mock_transcript()


def _mock_transcript() -> str:
    """
    Built-in demo transcript — app works fully without any audio file.
    """
    return """
Sarah: Good morning everyone. Let's get started with our weekly product sync.
Today we need to discuss the Q3 roadmap and assign owners for each initiative.

Rahul: The biggest priority right now is fixing the checkout bug
that's causing 15 percent cart abandonment. I can own that
and have a fix ready by Friday June 27th.

Sarah: Perfect. Rahul owns the checkout bug fix by Friday.
What about the new dashboard feature?

Priya: I'll take the dashboard. I need design specs first though.
Can someone send those over by Wednesday?

Sarah: I'll ping the design team today and make sure you get
specs by Wednesday June 25th. Priya your deadline for the
dashboard is July 5th. Does that work?

Priya: That works for me.

Rahul: Quick question — are we still doing the performance audit next week?

Sarah: Yes, let's schedule that for Tuesday June 24th at 2pm.
Rahul can you send calendar invites?

Rahul: Sure, I'll send invites today.

Sarah: One more thing — we need to update the API documentation.
That's been overdue for two weeks. Any volunteers?

Priya: I can do that after the dashboard specs come in.
I'll have the docs updated by July 10th.

Sarah: Excellent. Recap: Rahul fixes checkout bug by Friday
and sends calendar invites today. Priya builds dashboard by
July 5th and updates docs by July 10th. I'll get design specs
to Priya by Wednesday. Any questions?

Rahul: All clear from my side.
Priya: Same here. Good meeting everyone.
Sarah: Great, that's a wrap. Thanks everyone!
    """.strip()