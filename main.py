# main.py
from flask import Flask, render_template, request, jsonify, g
import os
from dotenv import load_dotenv
import google.generativeai as genai
from qa_data import QA_DATA
import sqlite3

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

# データベース接続
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('history.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_gemini_answer(question):
    print(f"質問: {question}")
<<<<<<< HEAD
=======
    # 以前の get_gemini_answer() 関数の中身をここに貼り付ける
>>>>>>> f0ca4b6 (Add history and persistence features)
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        print("Geminiモデルを初期化しました")

        qa_string = ""
        for key, value in QA_DATA.items():
            qa_string += f"### {key}\n{value}\n"
        
        full_question = f"""
        あなたはラルボットのカスタマーサポートAIです。
        以下の「ルール・規則」セクションに記載されている情報のみに基づいて、お客様からの質問に回答してください。
        **記載されていない質問には「申し訳ありませんが、その情報はこのQ&Aには含まれていません。」と答えてください。**
        お客様がスムーズに手続きを進められるよう、元気で丁寧な言葉遣いで案内してください。

        ---
        ## ルール・規則
        {qa_string}
        ---

        お客様の質問: {question}
        """
        print("Gemini APIにリクエストを送信します...")
        response = model.generate_content(full_question, request_options={'timeout': 30})
        print("Gemini APIから応答を受け取りました")

<<<<<<< HEAD
        print("Gemini APIにリクエストを送信します...")
        # APIリクエストにタイムアウトを30秒に設定
        response = model.generate_content(full_question, request_options={'timeout': 30})
        print("Gemini APIから応答を受け取りました")

=======
>>>>>>> f0ca4b6 (Add history and persistence features)
        if response and response.text:
            return response.text.strip()
        else:
            print("APIから応答がありませんでした。")
            return "申し訳ありませんが、その質問にはお答えできませんでした。別の質問をしてください。"

    except Exception as e:
<<<<<<< HEAD
        # エラーを詳細に表示
=======
>>>>>>> f0ca4b6 (Add history and persistence features)
        print(f"Gemini APIエラー: {type(e).__name__} - {e}")
        return "申し訳ありませんが、現在AIが応答できません。しばらくしてから再度お試しください。"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def get_history():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT sender, message FROM messages ORDER BY timestamp')
    history = [{'sender': row[0], 'message': row[1]} for row in cursor.fetchall()]
    return jsonify(history)

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'answer': '質問が空です。'})

<<<<<<< HEAD
=======
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (sender, message) VALUES (?, ?)", ('user', user_message))
    db.commit()

>>>>>>> f0ca4b6 (Add history and persistence features)
    bot_answer = get_gemini_answer(user_message)
    cursor.execute("INSERT INTO messages (sender, message) VALUES (?, ?)", ('bot', bot_answer))
    db.commit()
    
    return jsonify({'answer': bot_answer})

if __name__ == '__main__':
<<<<<<< HEAD
<<<<<<< HEAD
    # ポート番号を5001から5002に変更
    app.run(debug=True, port=5002)

=======
    app.run(debug=True, port=5002)
>>>>>>> f0ca4b6 (Add history and persistence features)
=======
    app.run(debug=True, port=5000)
>>>>>>> 29fb765 (Commit local changes before pulling)
