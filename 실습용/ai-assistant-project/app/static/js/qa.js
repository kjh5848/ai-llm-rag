/**
 * Q&A 실시간 채팅 로직 (AJAX)
 */
const chatHistory = document.getElementById('chatHistory');
const loadingIndicator = document.getElementById('loadingIndicator');
const queryInput = document.getElementById('queryInput');

function scrollToBottom() {
    if (chatHistory) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

async function submitQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    // 1. 사용자 메시지 추가
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chat-message user-message';
    userMsgDiv.innerHTML = `<div class="message-content">${query}</div>`;
    chatHistory.appendChild(userMsgDiv);
    
    // 입력창 초기화 및 스크롤
    queryInput.value = '';
    scrollToBottom();

    // 2. 로딩 표시 및 AI 답변 준비
    loadingIndicator.style.display = 'flex';

    try {
        const formData = new FormData();
        formData.append('query', query);

        // fetch 사용하여 AJAX 요청
        const response = await fetch('/admin/qa/query', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('서버 응답 오류');

        const html = await response.text();
        
        // 응답 HTML에서 AI 답변 블록만 추출하여 삽입
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        // AI 메시지는 chat-history의 마지막 ai-message 클래스
        const messages = doc.querySelectorAll('.chat-history .chat-message');
        const newAiMsg = messages[messages.length - 1];
        
        if (newAiMsg && newAiMsg.classList.contains('ai-message')) {
            chatHistory.appendChild(newAiMsg);
        } else {
            console.error("AI 응답을 파싱할 수 없습니다.");
        }

    } catch (error) {
        console.error('Error:', error);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'chat-message ai-message';
        errorDiv.innerHTML = `
            <div class="avatar">⚠️</div>
            <div class="message-content">오류가 발생했습니다. 다시 시도해 주세요. (${error.message})</div>
        `;
        chatHistory.appendChild(errorDiv);
    } finally {
        loadingIndicator.style.display = 'none';
        scrollToBottom();
    }
}

// 초기 스크롤 및 자동 하단 고정
window.onload = scrollToBottom;
