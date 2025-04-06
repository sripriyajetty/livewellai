// disease-chat.js
const chatBox = document.getElementById('chat-box');
const input = document.getElementById('user-input');

function addMessage(content, sender) {
  const msg = document.createElement('div');
  msg.className = sender === 'user' ? 'user-msg' : 'bot-msg';
  msg.innerText = content;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  
  addMessage(text, 'user');
  input.value = '';

  // 🔁 Replace this with API call to your Streamlit backend
  fetch('http://localhost:8501/symptom-check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ symptoms: text })
  })
  .then(res => res.json())
  .then(data => {
    addMessage(data.reply || "Sorry, I couldn’t understand that.", 'bot');
  })
  .catch(err => {
    console.error(err);
    addMessage("Oops! Couldn't reach the server.", 'bot');
  });
}
