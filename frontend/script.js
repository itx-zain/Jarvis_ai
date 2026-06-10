const micBtn = document.getElementById('mic-btn');
const micLabel = document.getElementById('mic-label');
const chatBox = document.getElementById('chat-box');
const visualizer = document.getElementById('visualizer');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

let isListening = false;

async function checkServer() {
    try {
        const res = await fetch('/status');
        if (res.ok) {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'Online';
        }
    } catch {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Offline';
    }
}

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.innerHTML = `<div class="bubble">${text}</div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function setUI(state) {
    if (state === 'listening') {
        micBtn.classList.add('listening');
        micLabel.textContent = 'Listening...';
        visualizer.classList.add('active');
        statusDot.className = 'status-dot listening';
        statusText.textContent = 'Listening...';
    } else if (state === 'processing') {
        micBtn.classList.add('listening');
        micLabel.textContent = 'Processing...';
        visualizer.classList.remove('active');
        statusDot.className = 'status-dot listening';
        statusText.textContent = 'Processing...';
    } else {
        micBtn.classList.remove('listening');
        micLabel.textContent = 'Click to Speak';
        visualizer.classList.remove('active');
        statusDot.className = 'status-dot online';
        statusText.textContent = 'Online';
        isListening = false;
    }
}

async function sendCommand(command) {
    try {
        const res = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command })
        });
        const data = await res.json();
        if (data.response) addMessage(data.response, 'jarvis');
    } catch {
        addMessage('Server se connect nahi ho saka.', 'jarvis');
    }
}

async function startVoiceListen() {
    if (isListening) return;
    isListening = true;
    setUI('listening');

    try {
        const res = await fetch('/listen', { method: 'POST' });
        const data = await res.json();

        if (data.status === 'busy') {
            addMessage('Pehle wali command process ho rahi hai...', 'jarvis');
            setUI('idle');
            return;
        }

        if (data.status === 'empty' || !data.command) {
            addMessage('Kuch suna nahi, dobara try karein.', 'jarvis');
            setUI('idle');
            return;
        }

        setUI('processing');
        addMessage(data.command, 'user');
        if (data.response) addMessage(data.response, 'jarvis');

    } catch {
        addMessage('Voice service se connect nahi ho saka.', 'jarvis');
    }

    setUI('idle');
}

function toggleListen() {
    if (!isListening) {
        startVoiceListen();
    }
}

// Text input
async function sendText() {
    const input = document.getElementById('text-input');
    const command = input.value.trim().toLowerCase();
    if (!command) return;
    input.value = '';
    addMessage(command, 'user');
    await sendCommand(command);
}

function handleKey(event) {
    if (event.key === 'Enter') sendText();
}

checkServer();
setInterval(checkServer, 5000);
