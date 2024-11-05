function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = chatContainer.style.display === "none" ? "block" : "none";
}

// Инициализация состояния чата при загрузке страницы
window.onload = function() {
    document.getElementById("chat-container").style.display = "none";
};
