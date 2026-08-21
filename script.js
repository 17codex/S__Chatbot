const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');

function addMessage(text, sender) {
  const div = document.createElement('div');
  div.className = 'msg ' + sender;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  userInput.value = '';

  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  });
  const data = await response.json();
  addMessage(data.reply, 'bot');
}

userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

addMessage("Hi! I'm your Student AI Chatbot. Ask me anything about studies, exams, or timetable.", 'bot');
