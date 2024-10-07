import os
from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/translate": {"origins": "https://study-project-steel.vercel.app"}})

# 翻訳する内容のテンプレート
TEMPLETE = """
### 指示:
下記の入力を日本語に翻訳して下さい。
入力:
__INPUT__
"""

# ChatGPTに質問する関数
def ask_chatgpt(prompt, model = "gpt-3.5-turbo"):
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

# githubとherokuを連携2
# 1.gunicornをrequirements.txtに追加
# 2.pip install -r requirements.txtでgunicornインストール
# 3.ターミナルでgunicorn app:app
# ※ app:appの最初のappはファイル名（app.pyのapp）、2番目のappはFlaskアプリケーションのインスタンス名（app = Flask(__name__)）です。
# 4.Profileにweb: gunicorn app:app　と記載
# 5.別ターミナルで下記３つ行う
# git add .
# git commit -m "Add gunicorn for production"
# git push heroku master

# 本番環境では app.run() を呼び出さない
# if __name__ == '__main__':
#     app.run(debug=True)
