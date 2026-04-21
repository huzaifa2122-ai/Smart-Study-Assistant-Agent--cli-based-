import os
import time
from google import genai

# 🔐 Secure API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# =========================
# 🔹 LLM CALL FUNCTION (WITH RETRY)
# =========================
def ask_llm(prompt):
    for i in range(3):  # retry 3 times
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"⚠️ Error: {e}")
            print(f"🔄 Retrying ({i+1}/3)...")
            time.sleep(5)

    return None


# =========================
# 🔹 AGENT FUNCTIONS
# =========================
def create_plan(topic):
    result = ask_llm(f"Break '{topic}' into 5 simple subtopics.")
    if not result:
        return "1. Basics\n2. Concepts\n3. Applications\n4. Examples\n5. Summary"
    return result


def explain_topic(subtopic):
    result = ask_llm(f"Explain '{subtopic}' simply with examples.")
    if not result:
        return "Explanation not available due to API issue."
    return result


# =========================
# 🔹 CHAT MODE
# =========================
def chat_mode():
    print("\n💬 Chat Mode (type 'exit' to quit)\n")
    while True:
        user = input("You: ")

        if user.lower() == "exit":
            break

        response = ask_llm(user)
        print("\n🤖:", response if response else "No response.")


# =========================
# 🔹 MAIN AGENT
# =========================
def run_agent():
    print("🤖 AI Productivity Agent\n")

    topic = input("Enter topic: ")

    print("\n📌 Generating plan...\n")
    plan = create_plan(topic)
    print(plan)

    if not plan:
        print("❌ Failed to generate plan.")
        return

    subtopics = [line.strip() for line in plan.split("\n") if line.strip()]
    notes = []

    print("\n📚 Explaining topics...\n")

    for sub in subtopics:
        print(f"\n🔹 {sub}")
        explanation = explain_topic(sub)
        print(explanation)
        notes.append(f"{sub}\n{explanation}")

    with open("notes.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(notes))

    print("\n✅ Notes saved to notes.txt")

    if input("\nEnter chat mode? (yes/no): ").lower() == "yes":
        chat_mode()


# =========================
if __name__ == "__main__":
    run_agent()