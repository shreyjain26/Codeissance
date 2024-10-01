function toggleChatbot() {
    const chatbot = document.getElementById("chatbot");
    chatbot.style.display = chatbot.style.display === "none" || chatbot.style.display === "" ? "flex" : "none";
}

function sendMessage() {
    const inputField = document.getElementById("chatbot-input-field");
    const message = inputField.value.trim();
    
    if (message === "") return;

    // Add user's message to the chat
    const chatMessages = document.getElementById("chatbot-messages");
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.innerText = "You: " + message;
    chatMessages.appendChild(userMessage);

    // Clear the input field
    inputField.value = "";

    // Send the message to the Flask backend
    fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Add the chatbot's response to the chat
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.innerText = "Bot: " + data.response;
        chatMessages.appendChild(botMessage);

        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
