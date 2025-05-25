from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import yaml
from .utils.tax_processor import TaxProcessor
from .utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Setup logging
logger = setup_logger()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize tax processor
tax_processor = TaxProcessor()

# HTML template for the chatbot interface
CHAT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>TaxAssist - Your Tax Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }
        .chat-container {
            width: 100%;
            height: 100vh;
            margin: 0;
            background: white;
            border-radius: 0;
            box-shadow: none;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            padding: 15px;
            text-align: center;
            flex-shrink: 0;
        }
        .header h1 {
            font-size: 2em;
            margin-bottom: 5px;
        }
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        .chat-box {
            flex: 1;
            height: auto;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #007bff;
        }
        button {
            padding: 12px 25px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background: #0056b3;
        }
        .message {
            margin: 10px 0;
            padding: 12px 16px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
            position: relative;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .bot-message {
            background: white;
            color: #333;
            margin-right: auto;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .typing-indicator {
            padding: 12px 16px;
            background: #e9ecef;
            border-radius: 15px;
            margin: 10px 0;
            display: none;
            align-items: center;
            max-width: 100px;
        }
        .typing-dot {
            width: 8px;
            height: 8px;
            background: #666;
            border-radius: 50%;
            margin: 0 3px;
            animation: typing 1s infinite ease-in-out;
        }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        @media (max-width: 600px) {
            .chat-container {
                width: 100%;
                margin: 0;
                border-radius: 0;
                height: 100vh;
            }
            .chat-box {
                height: calc(100vh - 180px);
            }
            .message {
                max-width: 90%;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>TaxAssist</h1>
            <p>Your AI Tax Assistant</p>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">
                Hi! I'm your AI tax assistant. How can I help you today?
            </div>
        </div>
        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
        <div class="input-area">
            <input type="text" 
                   id="userInput" 
                   placeholder="Ask me about taxes..." 
                   onkeypress="if(event.key === 'Enter') sendMessage()"
                   autocomplete="off">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const typingIndicator = document.getElementById('typingIndicator');
        const userInput = document.getElementById('userInput');

        function showTypingIndicator() {
            typingIndicator.style.display = 'flex';
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function hideTypingIndicator() {
            typingIndicator.style.display = 'none';
        }

        function appendMessage(message, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            // Ensure message is a string
            const messageText = typeof message === 'object' ? JSON.stringify(message) : String(message);
            messageDiv.textContent = messageText;
            
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            // Disable input while processing
            userInput.disabled = true;
            appendMessage(message, true);
            userInput.value = '';
            showTypingIndicator();

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: message })
                });
                
                const data = await response.json();
                hideTypingIndicator();
                
                if (data.error) {
                    appendMessage('Sorry, I encountered an error. Please try again.', false);
                } else {
                    appendMessage(data.response, false);
                }
            } catch (error) {
                hideTypingIndicator();
                appendMessage('Sorry, I encountered an error. Please try again.', false);
                console.error('Error:', error);
            } finally {
                // Re-enable input
                userInput.disabled = false;
                userInput.focus();
            }
        }

        // Handle Enter key
        userInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        // Focus input on page load
        userInput.focus();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    """Serve the chatbot interface"""
    return render_template_string(CHAT_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    """Process chat messages"""
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing query in request"}), 400

        # Get response from tax processor
        response = tax_processor.process_query(data["query"])
        
        # Ensure we return a string response
        if isinstance(response, dict):
            response_text = response.get('text', str(response))
        else:
            response_text = str(response)
            
        return jsonify({"response": response_text})

    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    port = int(os.getenv("PORT", config["server"]["port"]))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    app.run(
        host=config["server"]["host"],
        port=port,
        debug=debug
    ) 