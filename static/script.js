// script.js
document.addEventListener('DOMContentLoaded', () => {
    // 質問例ボタンがクリックされたときの処理
    document.querySelectorAll('.example-btn').forEach(button => {
        button.addEventListener('click', () => {
            const question = button.textContent;
            sendMessage(question);
        });
    });
});

async function sendMessage(message = null) {
    const userInput = document.getElementById('user-input');
    const userMessage = message || userInput.value.trim();

    if (userMessage === '') return;

    // ユーザーメッセージをチャット画面に追加
    addMessageToChat('user', userMessage);
    userInput.value = '';

    // ローディングメッセージを表示
    addMessageToChat('bot', '回答を生成中です...');

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error(`サーバーエラー: ${response.status}`);
        }

        const data = await response.json();
        
        // ローディングメッセージを削除
        document.querySelector('.bot-message:last-child').remove();
        
        // AIの回答をチャット画面に追加
        addMessageToChat('bot', data.answer);

    } catch (error) {
        console.error('Fetchエラー:', error);
        
        // ローディングメッセージを削除
        const loadingMessage = document.querySelector('.bot-message:last-child');
        if (loadingMessage) {
            loadingMessage.remove();
        }

        // タイムアウトやネットワークエラーの場合のメッセージ
        addMessageToChat('bot', '申し訳ありませんが、ネットワーク接続に問題が発生しました。しばらくしてから再度お試しください。');
    }
}

function addMessageToChat(sender, message) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
