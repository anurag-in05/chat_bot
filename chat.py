from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()
# Set up your Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the Flask app
app = Flask(__name__)

# Initialize the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Set up the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


@app.route("/chat", methods=["POST"])
def chat():
    # Get the user message from the request
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Start a chat session
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [user_message]},
            {"role": "model", "parts": ["Hi! How can I assist you today?"]},
        ]
    )

    # Get the model's response
    response = chat_session.send_message(user_message)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000)

