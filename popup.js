document.getElementById("send_message").addEventListener("click", async () => {
    const userMessage = document.getElementById("user_message").value;
    if (!userMessage) return;
  
    // Send the message to the Flask backend
    const response = await fetch("http://127.0.0.1:7000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userMessage })
    });
  
    const data = await response.json();
    
    // Display the model's response
    document.getElementById("response").textContent = data.response || "Error: " + data.error;
  });
  