# Student AI Chatbot - Python (console version)
# Run: python chatbot.py

knowledge_base = [
    {"keywords": ["hi", "hello", "hey"], "reply": "Hello! I'm your student assistant. Ask me about study tips, exams, or attendance."},
    {"keywords": ["timetable", "schedule"], "reply": "Check your college portal for the latest timetable. Want tips to plan a study schedule instead?"},
    {"keywords": ["exam", "test"], "reply": "For exams: revise short notes, solve previous year papers, and take 10-min breaks every hour."},
    {"keywords": ["study tips", "how to study", "concentration"], "reply": "Try the Pomodoro technique: 25 min focus + 5 min break. Repeat 4 times, then a longer break."},
    {"keywords": ["attendance"], "reply": "Most AKTU colleges require 75% attendance to sit for exams. Check with your department for exact rules."},
    {"keywords": ["marks", "grade", "result"], "reply": "Results are usually on the university/college portal. I can't fetch live data, but I can help you plan revision!"},
    {"keywords": ["bye", "thanks", "thank you"], "reply": "You're welcome! All the best for your studies."},
]

def get_bot_reply(user_input):
    text = user_input.lower()
    for item in knowledge_base:
        if any(keyword in text for keyword in item["keywords"]):
            return item["reply"]
    return "I'm a simple rule-based bot right now. Try asking about timetable, exams, study tips, attendance, or marks."

def main():
    print("Bot: Hi! I'm your Student AI Chatbot. Ask me anything about studies, exams, or timetable.")
    print("(Type 'quit' to exit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Bot: Goodbye! All the best.")
            break
        reply = get_bot_reply(user_input)
        print("Bot:", reply)

if __name__ == "__main__":
    main()
