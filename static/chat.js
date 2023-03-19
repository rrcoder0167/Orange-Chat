// Connect to the WebSocket server
const socket = io.connect();

// Emit a message to the server
socket.emit('message', { text: 'Hello World!' });

// Listen for incoming messages
socket.on('message', (data) => {
  console.log(data);
});

// Send a message to the server when the user submits a chat message
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

chatForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const message = chatInput.value.trim();
  if (message !== '') {
    socket.emit('message', message);
    socket.emit('receiver', /*RECIEVER ID HERE*/);
  }

  chatInput.value = '';
});

// Display the incoming messages on the chat window
const chatWindow = document.getElementById('chat-window');

socket.on('chatMessage', (message) => {
  const chatMessage = document.createElement('div');
  chatMessage.classList.add('chat-message');
  chatMessage.innerText = message;

  chatWindow.appendChild(chatMessage);
});
