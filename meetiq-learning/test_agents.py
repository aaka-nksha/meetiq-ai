from agents import run_meeting_agents

# Test with mock transcript
transcript = """
Sarah: Let's discuss Q3 targets.
Rahul: I'll fix the checkout bug by Friday.
Priya: I'll build the dashboard by July 5th.
Sarah: Great. Let's wrap up.
"""

results = run_meeting_agents(
    transcript=transcript,
    title="Q3 Sync",
    attendees=[]
)

print("✅ Agents working!")
print("\n📝 Summary:")
print(results["summary"])
print("\n✅ Action Items:")
for item in results["action_items"]:
    print(f"  - {item['task']} → {item['owner']} → {item['deadline']}")
print(f"\n📊 Health Score: {results['health_score']}/100")