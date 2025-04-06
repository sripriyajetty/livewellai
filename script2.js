// fitness-chat.js
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

  // Simple keyword-based responses (can upgrade to AI model later)
  const reply = getCoachResponse(text.toLowerCase());
  setTimeout(() => addMessage(reply, 'bot'), 500);
}

function getCoachResponse(input) {
  if (input.includes('weight loss')) {
    return "To lose weight, aim for a calorie deficit through cardio, strength training, and a balanced diet rich in protein and veggies.";
  } else if (input.includes('muscle gain') || input.includes('build muscle')) {
    return "To build muscle, focus on strength training 4–5 times a week, consume a high-protein diet, and get enough rest.";
  } else if (input.includes('flexibility') || input.includes('stretch')) {
    return "Incorporate daily stretching or yoga for flexibility. Try 10–15 minutes every morning or before bed.";
  } else if (input.includes('diet') || input.includes('nutrition')) {
    return "For a healthy diet, focus on whole foods: lean protein, complex carbs, healthy fats, fruits, and vegetables.";
  } else if (input.includes('routine') || input.includes('plan')) {
    return "Would you like a beginner, intermediate, or advanced routine? I can create one based on your level.";
  } else {
    return "Tell me your fitness goal like 'weight loss', 'muscle gain', or 'diet tips', and I’ll help you out!";
  }
}
