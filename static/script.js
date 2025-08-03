// script.js
document.addEventListener('DOMContentLoaded', () => {
    // ページ読み込み時に履歴を取得して表示
    loadHistory();
});

async function loadHistory() {
    try {
        const response = await fetch('/history');
        if (!response.ok) {
            throw new Error(`サーバーエラー: ${response.status}`);
        }
        const history = await response.json();
        history.forEach(item => {
            addMessageToChat(item.sender, item.message);
        });
    } catch (error) {
        console.error('Fetchエラー（履歴取得）:', error);
    }
}

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
        const loadingMessage = document.querySelector('.bot-message:last-child');
        if (loadingMessage) {
            loadingMessage.remove();
        }
        
        // AIの回答をチャット画面に追加
        addMessageToChat('bot', data.answer);

    } catch (error) {
        console.error('Fetchエラー:', error);
        
        const loadingMessage = document.querySelector('.bot-message:last-child');
        if (loadingMessage) {
            loadingMessage.remove();
        }

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
