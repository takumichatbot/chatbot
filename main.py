# main.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

def get_gemini_answer(question):
    print(f"質問: {question}")
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        print("Geminiモデルを初期化しました")
        
        full_question = f"""
        あなたは親切なAIアシスタントです。
        ユーザーからの質問に対して、簡潔で分かりやすい言葉で回答してください。

        ユーザーの質問: {question}
        """
        print("Gemini APIにリクエストを送信します...")
        response = model.generate_content(full_question, request_options={'timeout': 30})
        print("Gemini APIから応答を受け取りました")

        if response and response.text:
            return response.text.strip()
        else:
            print("APIから応答がありませんでした。")
            return "申し訳ありませんが、その質問にはお答えできませんでした。別の質問をしてください。"

    except Exception as e:
        print(f"Gemini APIエラー: {type(e).__name__} - {e}")
        return "申し訳ありませんが、現在AIが応答できません。しばらくしてから再度お試しください。"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'answer': '質問が空です。'})

    bot_answer = get_gemini_answer(user_message)
    
    return jsonify({'answer': bot_answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
