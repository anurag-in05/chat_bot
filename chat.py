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

# TUNED_MODEL_ID = 'tunedModels/spammodelgemini-a9q7ybtlpzm7'
# Generative model setup
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 512,
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
        print("recieved requesst")
        user_message = request.json.get("message")
        print("kuch to hai ")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        response = model.generate_content(user_message)

        print("Raw API Response:", response)

        # Extract text from response
        if response and response.candidates:
            bot_message = response.candidates[0].content.parts[0].text
            print("Final Response Text:", bot_message)
            return jsonify({"response": bot_message})
        else:
            print("Error: Invalid response structure")
            return jsonify({"error": "Invalid response from model"}), 500

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
