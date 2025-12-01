from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ⛑️ 建議：不要把 API Key 寫死在程式碼
# 設定環境變數：setx OPENAI_API_KEY "你的 Key"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise Exception("請先設定環境變數：OPENAI_API_KEY")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "user", "content": user_query}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    try:
        answer = result["choices"][0]["message"]["content"]
    except:
        answer = "⚠️ 無法解析 GPT 回覆：\n" + str(result)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    # host="0.0.0.0" 允許 Tableau 連線
    app.run(host="0.0.0.0", port=5000, debug=True)
