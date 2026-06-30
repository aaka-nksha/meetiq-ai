from gtts import gTTS

text = """
Sarah: Good morning everyone. Let's get started with our weekly product sync.
Today we need to discuss the Q3 roadmap and assign owners for each initiative.

Rahul: The biggest priority right now is fixing the checkout bug
that is causing fifteen percent cart abandonment.
I can own that and have a fix ready by Friday June 27th.

Sarah: Perfect. Rahul owns the checkout bug fix by Friday.
What about the new dashboard feature?

Priya: I will take the dashboard. I need design specs first though.
Can someone send those over by Wednesday?

Sarah: I will ping the design team today.
Priya your deadline for the dashboard is July 5th.

Rahul: Are we still doing the performance audit next week?

Sarah: Yes, Tuesday June 24th at 2pm.
Rahul can you send calendar invites?

Rahul: Sure, I will send invites today.

Sarah: One more thing, we need to update the API documentation.
Any volunteers?

Priya: I can do that after the dashboard specs come in.
I will have the docs updated by July 10th.

Sarah: Great. That is a wrap. Thanks everyone!
"""

tts = gTTS(text=text, lang='en')
tts.save("test_meeting.mp3")
print("✅ test_meeting.mp3 created!")