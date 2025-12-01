from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    image_base64 = data.get("image_base64")

    # -----------------------
    # Construct content list
    # -----------------------
    content_list = [
        {
            "type": "input_text",
            "text": message
        }
    ]

    if image_base64:
        content_list.append({
            "type": "input_image",
            "image_url": f"data:image/png;base64,{image_base64}"
        })

    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": content_list
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers=headers,
        json=payload
    )

    result = response.json()

    try:
        reply = result["output"][0]["content"][0]["text"]
    except:
        reply = f"API 格式錯誤：{result}"

    return jsonify({"reply": reply})
