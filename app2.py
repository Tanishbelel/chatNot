import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key="AIzaSyDsE6fqSN0MpYi3zNCtoZev6O-AxINcapY") 

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

app = Flask(__name__)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_sessions = {}

@app.route("/")
def index():
    return render_template('chat.html')  

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    session_id = request.form.get("session_id", "default")  

    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])

    
    response = chat_sessions[session_id].send_message(user_input)

    
    bot_response = response.text

    return jsonify({"response": bot_response})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
