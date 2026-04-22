#!/usr/bin/env python3
"""
CogniDREAM Agent - Let's build an HR benefits portal for all employees to access. It must be properly secured and personalized to each employee's benefits. Please ask me follow up questions before executing.
"""
from flask import Flask, jsonify, request, render_template_string
import requests
import json

app = Flask(__name__)

LLAMA_URL = "http://localhost:8000/v1/chat/completions"
LLAMA_MODEL = "Meta-Llama-3-8B-Instruct-Q4_K_M"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CogniDREAM AI - Let's build an HR benefits portal for all employees to access. It must be properly secured and personalized to each employee's benefits. Please ask me follow up questions before executing.</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #0d0d0d 100%); min-height: 100vh; color: #e0e0e0; }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        h1 { color: #00d9ff; text-align: center; margin-bottom: 10px; font-size: 2.5em; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; }
        .status { text-align: center; padding: 10px; background: #1a1a2e; border-radius: 8px; margin-bottom: 20px; font-size: 12px; }
        .status.online { color: #00ff88; }
        .chat-box { background: #1a1a2e; border-radius: 16px; padding: 20px; border: 1px solid #2a2a4a; }
        .messages { height: 400px; overflow-y: auto; margin-bottom: 20px; }
        .message { padding: 12px 16px; margin-bottom: 12px; border-radius: 12px; max-width: 80%; }
        .message.user { background: #00d9ff20; color: #00d9ff; margin-left: auto; }
        .message.assistant { background: #1a1a2e; color: #e0e0e0; }
        .message.thinking { color: #666; font-style: italic; }
        .input-area { display: flex; gap: 10px; }
        input { flex: 1; padding: 14px 18px; border-radius: 8px; border: 1px solid #2a2a4a; background: #0d0d0d; color: #e0e0e0; font-size: 14px; }
        input:focus { outline: none; border-color: #00d9ff; }
        button { padding: 14px 28px; border-radius: 8px; border: none; background: linear-gradient(135deg, #00d9ff, #00b8d4); color: #0d0d0d; font-weight: 600; cursor: pointer; }
        button:hover { box-shadow: 0 0 20px rgba(0,217,255,0.4); }
        button:disabled { background: #333; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CogniDREAM AI</h1>
        <p class="subtitle">Let's build an HR benefits portal for all employees to access. It must be properly secured and personalized to each employee's benefits. Please ask me follow up questions before executing.</p>
        <div class="status online">AI Ready - Powered by Llama 3</div>
        <div class="chat-box">
            <div class="messages" id="messages">
                <div class="message assistant">Hello! I'm your CogniDREAM AI assistant. How can I help you today?</div>
            </div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type your message..." onkeypress="if(event.key==='Enter')sendMessage()">
                <button id="sendBtn" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const btn = document.getElementById('sendBtn');
            const msg = input.value.trim();
            if (!msg) return;
            
            addMessage(msg, 'user');
            input.value = '';
            btn.disabled = true;
            
            const thinking = addMessage('Thinking...', 'thinking');
            
            try {
                const resp = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await resp.json();
                thinking.remove();
                addMessage(data.response, 'assistant');
            } catch(e) {
                thinking.remove();
                addMessage('Error: ' + e.message, 'thinking');
            }
            btn.disabled = false;
        }
        
        function addMessage(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            div.scrollIntoView();
            return div;
        }
    </script>
</body>
</html>
"""

def query_llama(prompt):
    try:
        resp = requests.post(LLAMA_URL, json={
            "model": LLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }, timeout=120)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, I'm having trouble connecting to the AI. Please check if the LLM server is running."
    return "Sorry, I'm having trouble connecting to the AI."

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    response = query_llama(user_msg)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
