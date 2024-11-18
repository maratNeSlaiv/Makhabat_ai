const chatTextInput = document.getElementById('chat-text-input');

function resizeTextArea() {
    chatTextInput.style.height = 'auto';
    const maxHeight = parseInt(chatTextInput.style.maxHeight, 10);
    const newHeight = Math.min(chatTextInput.scrollHeight, maxHeight); 
    chatTextInput.style.height = newHeight + 'px';
}

chatTextInput.addEventListener('input', resizeTextArea);
resizeTextArea();


recordAudioButton = document.getElementById("record-audio-button")
recordAudioButton.addEventListener("click", function() {
    this.classList.toggle("recording");
});
