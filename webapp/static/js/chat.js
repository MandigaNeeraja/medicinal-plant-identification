function getParameterByName(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function addChatBubble(text, role) {
    const chatMessages = document.getElementById('chatMessages');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role === 'user' ? 'user-bubble' : 'assistant-bubble'}`;
    bubble.innerHTML = text;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function renderSuggestions(suggestions) {
    const suggestionsWrapper = document.getElementById('chatSuggestions');
    suggestionsWrapper.innerHTML = '';
    if (!suggestions || suggestions.length === 0) {
        return;
    }

    const title = document.createElement('div');
    title.className = 'suggestions-title';
    title.textContent = 'Suggested questions:';
    suggestionsWrapper.appendChild(title);

    const list = document.createElement('div');
    list.className = 'suggestions-list';

    suggestions.forEach(s => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'suggestion-btn btn btn-secondary';
        btn.textContent = s;
        btn.addEventListener('click', () => {
            document.getElementById('chatInput').value = s;
            sendChatMessage();
        });
        list.appendChild(btn);
    });

    suggestionsWrapper.appendChild(list);
}

async function initChat(plantName) {
    try {
        const response = await fetch('/chat/init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plant_name: plantName })
        });

        const data = await response.json();
        if (data.success) {
            addChatBubble(`💬 Chat created for <strong>${plantName}</strong>`, 'assistant');
            if (data.summary && data.summary.overview) {
                addChatBubble(`<strong>Summary:</strong> ${data.summary.overview}`, 'assistant');
            }
            if (data.suggestions) {
                renderSuggestions(data.suggestions);
            }
        } else {
            addChatBubble(`Error: ${data.error || 'Could not initialize chat'}`, 'assistant');
        }
    } catch (error) {
        addChatBubble(`Error: ${error.message}`, 'assistant');
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();
    if (!question) return;

    addChatBubble(question, 'user');
    input.value = '';

    try {
        const res = await fetch('/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: question })
        });
        const data = await res.json();
        if (data.success) {
            addChatBubble(data.answer, 'assistant');
            renderSuggestions(data.suggestions || []);
        } else {
            addChatBubble(`Assistant error: ${data.error || 'No response'}`, 'assistant');
        }
    } catch (err) {
        addChatBubble(`Assistant error: ${err.message}`, 'assistant');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const plantName = getParameterByName('plant_name');
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSendBtn');
    if (!plantName) {
        addChatBubble('No plant specified. Please return to the main page and pick a plant.', 'assistant');
        input.disabled = true;
        sendBtn.disabled = true;
        return;
    }

    initChat(plantName);

    sendBtn.addEventListener('click', sendChatMessage);
    input.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            sendChatMessage();
        }
    });
});