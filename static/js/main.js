// Toggle chat window visibility
const chatToggleButton = document.getElementById('chat-toggle-button');
const chatWindow = document.getElementById('chat-window'); // Ensure this matches the id in HTML

chatToggleButton.addEventListener("click", () => {
  chatWindow.classList.toggle("show"); // This toggles the chat window's visibility
});
