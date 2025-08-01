# main.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Google Gemini API のインポート
import google.generativeai as genai

# qa_data.pyからQ&Aデータをインポート
from qa_data import QA_DATA

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得し、Gemini APIを設定
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

def get_gemini_answer(question):
    """
    Google Gemini APIを使用して、事前に定義されたルールに基づいて回答を生成する関数
    """
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        # 辞書を文字列に変換してプロンプトに組み込む
        qa_string = ""
        for key, value in QA_DATA.items():
            qa_string += f"### {key}\n{value}\n"
        
        # プロンプトを詳細化し、QAデータを含める
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

        # AIに質問を送信し、回答を生成
        response = model.generate_content(full_question) 

        # 応答からテキストを抽出
        if response.parts:
            if hasattr(response, 'text'):
                return response.text.strip()
            elif response.parts and hasattr(response.parts[0], 'text'):
                return response.parts[0].text.strip()
        
        return "申し訳ありませんが、その質問にはお答えできませんでした。別の質問をしてください。"

    except Exception as e:
        print(f"Gemini APIエラー: {e}")
        return "申し訳ありませんが、現在AIが応答できません。しばらくしてから再度お試しください。"


@app.route('/')
def index():
    """
    チャットボットのメインページ（UI全体）を表示
    """
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    """
    ユーザーからの質問を受け取り、AIが回答を返すAPIエンドポイント
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'answer': '質問が空です。'})

    # Gemini AIを使って回答を生成
    bot_answer = get_gemini_answer(user_message)
    return jsonify({'answer': bot_answer})

# main.py
# ... (省略) ...

if __name__ == '__main__':
    app.run(debug=True, port=5001)

