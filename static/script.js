document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');

    sendBtn.addEventListener('click', () => {
        sendMessage();
    });

    voiceBtn.addEventListener('click', () => {
        recordVoice();
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value;
        if (message.trim() !== '') {
            appendMessage('user', message);
            userInput.value = '';

            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: message })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage('bot', data.response);
            });
        }
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function recordVoice() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                userInput.value = transcript;
                appendMessage(userInput.value);
            };

            recognition.onerror = function(event) {
                console.error("Error in speech recognition: ", event);
                alert("Speech recognition error. Please try again.");
            };

            recognition.start();
        } else {
            alert("Your browser does not support Web Speech API.");
        }
    }
});
