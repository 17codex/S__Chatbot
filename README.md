# Student AI Chatbot

Simple rule-based chatbot for students — built with HTML, CSS, JS. Works fully offline, no API key needed.

## Run in VS Code
1. Extract zip, open folder in VS Code.
2. Install "Live Server" extension (optional).
3. Right-click `index.html` → "Open with Live Server" (or just open the file in a browser).

## Structure
- `index.html` — UI layout
- `style.css` — styling
- `script.js` — chatbot logic (keyword-based replies)

## Upgrade ideas
- Replace `getBotReply()` logic with a real AI API call (e.g., Anthropic/OpenAI) for smarter answers.
- Add more keywords/replies in `knowledgeBase` array in `script.js`.
- Add voice input using Web Speech API.
