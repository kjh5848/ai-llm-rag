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

/**
 * 채팅 내역을 localStorage에 저장
 */
function saveChatHistory() {
    const messages = [];
    const messageElements = chatHistory.querySelectorAll('.chat-message');
    
    messageElements.forEach(el => {
        messages.push({
            className: el.className,
            innerHTML: el.innerHTML
        });
    });
    
    localStorage.setItem('metacoding_chat_history', JSON.stringify(messages));
}

/**
 * localStorage에서 채팅 내역 로드
 */
function loadChatHistory() {
    const saved = localStorage.getItem('metacoding_chat_history');
    if (!saved || !chatHistory) return;
    
    try {
        const messages = JSON.parse(saved);
        chatHistory.innerHTML = ''; // 초기화 후 다시 채움
        messages.forEach(msg => {
            const div = document.createElement('div');
            div.className = msg.className;
            div.innerHTML = msg.innerHTML;
            chatHistory.appendChild(div);
        });
        scrollToBottom();
    } catch (e) {
        console.error("Failed to load chat history:", e);
    }
}

/**
 * 채팅 내력 비우기
 */
function clearChatHistory() {
    if (confirm("대화 내역을 모두 지우시겠습니까?")) {
        localStorage.removeItem('metacoding_chat_history');
        if (chatHistory) chatHistory.innerHTML = '';
    }
}

async function submitQuery(event) {
    if (event) event.preventDefault(); // 폼 기본 제출 방지

    const query = queryInput.value.trim();
    if (!query) return;

    // 1. 사용자 메시지 추가
    // ... (기존 로직 유지)
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chat-message user-message';
    userMsgDiv.innerHTML = `<div class="message-content">${query}</div>`; // XSS 방지를 위해 textContent 권장하나 기존 유지
    userMsgDiv.querySelector('.message-content').textContent = query; // 안전하게 텍스트만 삽입
    chatHistory.appendChild(userMsgDiv);
    
    // 입력창 초기화
    queryInput.value = '';
    
    // ... (이하 로직 동일)
    saveChatHistory();
    scrollToBottom();

    // 2. 로딩 표시 및 AI 답변 준비
    loadingIndicator.style.display = 'flex';

    try {
        const isAgentMode = document.getElementById('agentModeToggle').checked;
        const endpoint = isAgentMode ? '/admin/qa/agent' : '/admin/qa/query';

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) throw new Error('서버 응답 오류');

        const data = await response.json();
        
        // 3. AI 답변 표시
        const aiMsgDiv = document.createElement('div');
        aiMsgDiv.className = 'chat-message ai-message';
        
        let content = data.answer || "답변을 가져올 수 없습니다.";
        // 줄바꿈 처리
        content = content.replace(/\n/g, '<br />');
        
        aiMsgDiv.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="message-content">
                <div class="ai-ans-text">${content}</div>
                ${data.mode === 'agent' ? '<small style="color:#666; display:block; margin-top:10px;">⚡ Agent Mode 실행됨</small>' : ''}
            </div>
        `;
        
        chatHistory.appendChild(aiMsgDiv);
        saveChatHistory();

    } catch (error) {
        console.error('Error:', error);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'chat-message ai-message';
        errorDiv.innerHTML = `
            <div class="avatar">⚠️</div>
            <div class="message-content">오류가 발생했습니다. 다시 시도해 주세요. (${error.message})</div>
        `;
        chatHistory.appendChild(errorDiv);
        saveChatHistory();
    } finally {
        loadingIndicator.style.display = 'none';
        scrollToBottom();
    }
}

// 초기 로드 시 내역 불러오기 및 스크롤
window.addEventListener('DOMContentLoaded', () => {
    // 저장된 내역이 있으면 불러와서 표시 (기존 SSR 내용 덮어쓰기)
    const saved = localStorage.getItem('metacoding_chat_history');
    if (saved) {
        loadChatHistory();
    }
    scrollToBottom();
});

// 이벤트 리스너 수정
// 폼 제출 이벤트로 통일 (엔터키도 기본적으로 폼 제출을 트리거함)
const qaForm = document.getElementById('qaForm');
if (qaForm) {
    qaForm.addEventListener('submit', submitQuery);
}

// 기존 엔터키 리스너 제거 (필요 없음)
// window load 시 리스너 등록 방식 변경
