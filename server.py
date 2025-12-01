from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/api/chat", methods=["POST"])
def chat():

    message = request.form.get("message", "")
    image_file = request.files.get("image")

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    # 如果有圖片，走 Vision 模式
    if image_file:
        files = {
            "image": (image_file.filename, image_file.stream, image_file.mimetype)
        }

        payload = {
            "model": "gpt-4.1-mini",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {"type": "input_image", "image": {"input": "image"}}
                    ]
                }
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers=headers,
            data={"data": str(payload)},
            files=files
        )

    else:
        # 純文字模式
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={**headers, "Content-Type": "application/json"},
            json={"model": "gpt-4.1-mini", "input": message}
        )

    result = response.json()

    try:
        reply = result["output"][0]["content"][0]["text"]
    except:
        reply = f"API 格式錯誤：{result}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
