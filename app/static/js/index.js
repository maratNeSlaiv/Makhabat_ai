function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
        document.getElementById('theme-toggle').textContent = '🌙'; // Значок для светлой темы
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-toggle').textContent = '☀️'; // Значок для темной темы
    }
}

function appendMessage(sender, message) {
    let chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML += `<p><b>${sender}:</b> ${message}</p>`;
}

async function sendMessage(message = null) {
    const userMessage = message || document.getElementById('user-input').value;

    // Сбрасываем текстовое поле ввода перед отправкой сообщения
    document.getElementById('user-input').value = '';

    // Добавляем сообщение только если оно не из аудиозаписи
    if (!message) {
        appendMessage("Вы", userMessage);
    }

    const response = await fetch('/send_message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: userMessage})
    });
    const data = await response.json();
    appendMessage("Алгоритм", data.response);
}

async function startRecording() {
    await fetch('/start_recording', {method: 'POST'});
}

async function stopRecording() {
    const response = await fetch('/stop_recording', {method: 'POST'});
    const data = await response.json();
    if (data.text) {
        appendMessage("Вы (аудио)", data.text);  // Показать текст из аудио
        sendMessage(data.text);  // Отправить текст как сообщение
    }
}

