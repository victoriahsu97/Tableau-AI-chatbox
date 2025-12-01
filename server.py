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

    message = request.form.get("message", "")
    image_file = request.files.get("image")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # --------------------------
    #  1) 有圖片：使用 Vision 模式
    # --------------------------
    if image_file:

        # Payload 格式需為字串（因 multipart/form-data 不接受 JSON object）
        vision_payload = {
            "model": "gpt-4.1-mini",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {
                            "type": "input_image",
                            "image": {"input": "image"}   # 告訴 OpenAI 圖片在 form-data 裡
                        }
                    ]
                }
            ]
        }

        files = {
            "image": (
                image_file.filename,
