// Function to handle sending messages
async function sendMessage() {
  const inputBox = document.getElementById("messageInput");
  const chatbox = document.getElementById("chatbox");

  const userMessage = inputBox.value.trim();
  if (!userMessage) {
    alert("Please enter a message."); // Ensure input isn't empty
    return;
  }

  // Display the user's message in the chatbox
  const userDiv = document.createElement("div");
  userDiv.className = "user";
  userDiv.innerText = `You: ${userMessage}`;
  chatbox.appendChild(userDiv);

  try {
    // Send the user's message to the Flask backend
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();

    // Display the bot's response in the chatbox
    const botDiv = document.createElement("div");
    botDiv.className = "bot";
    botDiv.innerText = `Bot: ${data.response}`;
    chatbox.appendChild(botDiv);
  } catch (error) {
    // Handle errors (e.g., network issues, backend not running)
    const errorDiv = document.createElement("div");
    errorDiv.className = "bot";
    errorDiv.innerText = "Error: Unable to connect to the server.";
    chatbox.appendChild(errorDiv);
    console.error("Error:", error);
  }

  // Clear the input box and scroll chatbox to the bottom
  inputBox.value = "";
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Attach the sendMessage function to the Send button
document.querySelector("button").addEventListener("click", sendMessage);

// Optionally, allow pressing "Enter" to send a message
document.getElementById("messageInput").addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});
