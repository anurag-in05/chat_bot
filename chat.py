from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create Flask app
app = Flask(__name__)

# Generative model setup
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the AI Chat API. Use the /chat endpoint to interact."})

@app.route("/ask", methods=["POST"])
def ask():
    # Your logic here
    return jsonify({"response": "This is a response"})



@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the user message from the request
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Initialize model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start a chat session
        chat_session = model.start_chat(
            history=[
                {"role": "user", "parts": [user_message]},
                {"role": "model", "parts": ["Hi! How can I assist you today?"]},
            ]
        )

        # Get model response
        response = chat_session.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
