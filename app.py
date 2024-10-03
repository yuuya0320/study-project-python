from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 翻訳する内容のテンプレート
TEMPLETE = """
### 指示:
下記の入力を日本語に翻訳して下さい。
入力:
__INPUT__
"""

# ChatGPTに質問する関数
def ask_chatgpt(prompt, model = "gpt-3.5-turbo"):
  client = OpenAI()
  completion = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}]
  )
  return completion.choices[0].message.content

# ルートに対応するハンドラ
@app.route('/')
def home():
  return "Flaskサーバーが正しく動作しています！"

@app.route('/translate', methods=['POST'])
def translate():
  data = request.json
  text_english = data.get('text')
  prompt = TEMPLETE.replace("__INPUT__", text_english)
  result = ask_chatgpt(prompt)
  print(result)
  return jsonify(translatedText=result)

if __name__ == '__main__':
    app.run(debug=True)
