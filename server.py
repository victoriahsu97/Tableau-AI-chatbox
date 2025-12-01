from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ← 這行非常重要，允許跨域！

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": user_message}]
        }
    )

    return jsonify(r.json())

@app.route("/")
def home():
    return "ChatGPT proxy server is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
