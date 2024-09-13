// Select elements
const chatbox = document.querySelector('.chatbox');
const inputField = document.querySelector('.chatbox__footer input');
const sendButton = document.querySelector('.send__button');
const darkModeToggle = document.querySelector('.dark-mode-toggle');
const closeButtonInside = document.querySelector('.chatbox__close-button');
const popupChatboxToggle = document.querySelector('.popup-chatbox-toggle');

// Toggle dark mode
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    chatbox.classList.toggle('dark-mode');
});

// Handle sending messages
sendButton.addEventListener('click', async () => {
    const message = inputField.value.trim();
    if (message) {
        // Append user message
        appendMessage('visitor', message);
        inputField.value = '';

        // Show thinking message
        appendMessage('operator', 'Chatbot thinking...');

        // Send message to server
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Replace thinking message with actual response
            const messages = chatbox.querySelectorAll('.messages__item--operator');
            if (messages.length && messages[messages.length - 1].innerText === 'Chatbot thinking...') {
                messages[messages.length - 1].remove();
            }
            
            appendMessage(data.source.toLowerCase(), data.message);
        } catch (error) {
            console.error('Error:', error);
        }
    }
});

// Append messages to chatbox
function appendMessage(source, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('messages__item', `messages__item--${source}`);
    messageElement.innerText = message;
    chatbox.querySelector('.chatbox__messages').appendChild(messageElement);
    chatbox.querySelector('.chatbox__messages').scrollTop = chatbox.querySelector('.chatbox__messages').scrollHeight; // Scroll to the bottom
}

// Close chatbox
closeButtonInside.addEventListener('click', () => {
    chatbox.style.display = 'none';
    popupChatboxToggle.style.display = 'block'; // Show popup button
});

// Toggle chatbox visibility
popupChatboxToggle.addEventListener('click', () => {
    if (chatbox.style.display === 'none' || !chatbox.style.display) {
        chatbox.style.display = 'flex';
        popupChatboxToggle.style.display = 'none'; // Hide popup button
    } else {
        chatbox.style.display = 'none';
        popupChatboxToggle.style.display = 'block'; // Show popup button
    }
});

// Initial chatbox load
appendMessage('operator', 'Hello! I am BharatAi, How can I assist you today?');
