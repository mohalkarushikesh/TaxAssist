document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendMessage');
    const clearButton = document.getElementById('clearChat');
    const escalateButton = document.getElementById('escalateToHuman');
    let isTyping = false;

    // Handle sending messages
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message || isTyping) return;

        // Add user message to chat
        appendMessage('user', message);
        userInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            
            // Remove typing indicator and add bot response
            removeTypingIndicator();
            
            if (response.ok) {
                appendMessage('bot', data.response);
            } else {
                appendMessage('error', data.error || 'Something went wrong. Please try again.');
            }
        } catch (error) {
            removeTypingIndicator();
            appendMessage('error', 'Network error. Please check your connection and try again.');
        }
    };

    // Append a message to the chat
    const appendMessage = (type, content) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start';

        const iconDiv = document.createElement('div');
        iconDiv.className = 'flex-shrink-0';
        
        const iconWrapper = document.createElement('div');
        iconWrapper.className = `w-8 h-8 rounded-full flex items-center justify-center ${
            type === 'user' ? 'bg-gray-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'
        }`;

        const icon = document.createElement('i');
        icon.className = `fas ${
            type === 'user' ? 'fa-user' : type === 'error' ? 'fa-exclamation-triangle' : 'fa-robot'
        } text-white`;

        iconWrapper.appendChild(icon);
        iconDiv.appendChild(iconWrapper);
        messageDiv.appendChild(iconDiv);

        const contentDiv = document.createElement('div');
        contentDiv.className = 'ml-3 bg-white rounded-lg p-4 shadow-sm max-w-3xl';
        contentDiv.innerHTML = `<p class="text-gray-800">${content}</p>`;
        messageDiv.appendChild(contentDiv);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Show typing indicator
    const showTypingIndicator = () => {
        isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'flex items-start';
        typingDiv.innerHTML = `
            <div class="flex-shrink-0">
                <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                    <i class="fas fa-robot text-white"></i>
                </div>
            </div>
            <div class="ml-3 bg-white rounded-lg p-4 shadow-sm">
                <div class="flex space-x-2">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Remove typing indicator
    const removeTypingIndicator = () => {
        isTyping = false;
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    };

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    clearButton.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        // Add welcome message back
        appendMessage('bot', 'Hello! I\'m TaxAssist, your property tax expert from Cotality. How can I help you today?');
    });

    escalateButton.addEventListener('click', () => {
        window.location.href = 'mailto:supportUK@cotality.com?subject=TaxAssist%20Escalation';
    });

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
    });
}); 