from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 從環境變數讀取 OPENAI API KEY（Render 會提供）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("請先設定環境變數：OPENAI_API_KEY")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": data["question"]}]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    result = response.json()

    return jsonify({
        "answer": result["choices"][0]["message"]["content"]
    })

# ✔ Render 必須使用環境變數 PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 自動提供 PORT
    app.run(host="0.0.0.0", port=port)
