class AIChatbot {
  constructor() {
    this.isOpen = false;
    this.messages = [];
    this.unreadCount = 0;
    this.isTyping = false;
    this.currentLanguage = 'en'; 
    this.init();
  }
  init() {
    this.setupEventListeners();
    this.clearConversationHistory(); 
    this.loadLanguagePreference();
  }
  setupEventListeners() {
    document.getElementById('chatbot-toggle').addEventListener('click', () => {
      this.toggleChat();
    });
    document.getElementById('chatbot-close').addEventListener('click', () => {
      this.closeChat();
    });
    const dropdownBtn = document.getElementById('language-dropdown-btn');
    const dropdown = document.getElementById('language-dropdown');
    const dropdownArrow = document.getElementById('dropdown-arrow');
    dropdownBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = !dropdown.classList.contains('hidden');
      if (isOpen) {
        dropdown.classList.add('hidden');
        dropdownArrow.style.transform = 'rotate(0deg)';
      } else {
        dropdown.classList.remove('hidden');
        dropdownArrow.style.transform = 'rotate(180deg)';
      }
    });
    const languageOptions = document.querySelectorAll('.language-option');
    languageOptions.forEach(option => {
      option.addEventListener('click', (e) => {
        e.stopPropagation();
        const lang = option.dataset.lang;
        const flag = option.dataset.flag;
        this.changeLanguage(lang, flag);
        dropdown.classList.add('hidden');
        dropdownArrow.style.transform = 'rotate(0deg)';
      });
    });
    document.addEventListener('click', (e) => {
      if (!dropdownBtn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add('hidden');
        dropdownArrow.style.transform = 'rotate(0deg)';
      }
    });
    document.getElementById('chatbot-form').addEventListener('submit', (e) => {
      e.preventDefault();
      this.sendMessage();
    });
    document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
    document.addEventListener('click', (e) => {
      const chatbotContainer = document.getElementById('chatbot-container');
      if (!chatbotContainer.contains(e.target) && this.isOpen) {
        this.closeChat();
      }
    });
  }
  toggleChat() {
    if (this.isOpen) {
      this.closeChat();
    } else {
      this.openChat();
    }
  }
  openChat() {
    const chatWindow = document.getElementById('chatbot-window');
    const toggleBtn = document.getElementById('chatbot-toggle');
    chatWindow.classList.remove('hidden');
    toggleBtn.classList.add('hidden');
    this.isOpen = true;
    this.markAsRead();
    setTimeout(() => {
      document.getElementById('chatbot-input').focus();
    }, 300);
  }
  closeChat() {
    const chatWindow = document.getElementById('chatbot-window');
    const toggleBtn = document.getElementById('chatbot-toggle');
    chatWindow.classList.add('hidden');
    toggleBtn.classList.remove('hidden');
    this.isOpen = false;
  }
  async sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    if (!message || this.isTyping) return;
    this.addMessage(message, 'user');
    input.value = '';
    this.showTypingIndicator();
    try {
      const response = await this.getBotResponse(message);
      this.hideTypingIndicator();
      this.addMessage(response, 'bot');
    } catch (error) {
      this.hideTypingIndicator();
      this.addMessage('Sorry, I encountered an error. Please try again later.', 'bot');
    }
  }
  addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex items-start gap-3 chat-message ${sender === 'user' ? 'flex-row-reverse' : ''}`;
    if (sender === 'user') {
      messageDiv.innerHTML = `
        <div class="bg-gradient-to-r from-primary to-secondary text-white rounded-2xl rounded-tr-none p-3 shadow-sm max-w-[80%]">
          <p class="text-sm">${this.escapeHtml(text)}</p>
          <span class="text-xs opacity-75 mt-1 block">${timestamp}</span>
        </div>
        <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
        </div>
      `;
    } else {
      messageDiv.innerHTML = `
        <div class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-sm max-w-[80%]">
          <p class="text-sm text-gray-700">${text}</p>
          <span class="text-xs text-gray-400 mt-1 block">${timestamp}</span>
        </div>
      `;
    }
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    this.messages.push({ text, sender, timestamp });
    if (!this.isOpen && sender === 'bot') {
      this.updateUnreadCount();
    }
  }
  showTypingIndicator() {
    this.isTyping = true;
    document.getElementById('typing-indicator').classList.remove('hidden');
    document.getElementById('send-button').disabled = true;
    const messagesContainer = document.getElementById('chatbot-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
  hideTypingIndicator() {
    this.isTyping = false;
    document.getElementById('typing-indicator').classList.add('hidden');
    document.getElementById('send-button').disabled = false;
  }
  async getBotResponse(message) {
    try {
      const response = await fetch('/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: message,
          language: this.currentLanguage 
        }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      if (data.language && data.language !== this.currentLanguage) {
        this.currentLanguage = data.language;
        this.updateLanguageSelector();
        this.saveLanguagePreference();
      }
      return data.response;
    } catch (error) {
      console.error('Chatbot error:', error);
      const fallbackResponses = {
        'en': "I'm sorry, I'm having trouble connecting right now. Please try again later.",
        'es': "Lo siento, estoy teniendo problemas de conexión. Por favor, inténtalo más tarde.",
        'zh': "对不起，我现在连接有问题。请稍后再试。"
      };
      return fallbackResponses[this.currentLanguage] || fallbackResponses['en'];
    }
  }
  updateUnreadCount() {
    this.unreadCount++;
    const badge = document.getElementById('unread-badge');
    badge.textContent = this.unreadCount;
    badge.classList.remove('hidden');
  }
  markAsRead() {
    this.unreadCount = 0;
    const badge = document.getElementById('unread-badge');
    badge.classList.add('hidden');
  }
  clearConversationHistory() {
    try {
      localStorage.removeItem('chatbot_history');
    } catch (error) {
      console.error('Failed to clear conversation history:', error);
    }
    this.messages = [];
    this.unreadCount = 0;
    const messagesContainer = document.getElementById('chatbot-messages');
    const allMessages = messagesContainer.children;
    if (allMessages.length > 1) {
      for (let i = allMessages.length - 1; i > 0; i--) {
        allMessages[i].remove();
      }
    }
  }
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  changeLanguage(language, flag = null) {
    this.currentLanguage = language;
    this.saveLanguagePreference();
    this.updateLanguageSelector(flag);
    const messagesContainer = document.getElementById('chatbot-messages');
    const notification = document.createElement('div');
    notification.className = 'text-center text-xs text-gray-500 italic my-2';
    notification.textContent = this.getLanguageChangeMessage(language);
    messagesContainer.appendChild(notification);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
  updateLanguageSelector(flag = null) {
    const currentFlag = document.getElementById('current-flag');
    const currentLang = document.getElementById('current-lang');
    if (flag) {
      currentFlag.src = flag;
      currentFlag.alt = this.getLanguageName(this.currentLanguage);
    } else {
      const flags = {
        'en': '/static/images/flags/us.svg',
        'es': '/static/images/flags/es.svg',
        'zh': '/static/images/flags/cn.svg'
      };
      currentFlag.src = flags[this.currentLanguage] || flags['en'];
      currentFlag.alt = this.getLanguageName(this.currentLanguage);
    }
    const langNames = {
      'en': 'EN',
      'es': 'ES',
      'zh': '中文'
    };
    currentLang.textContent = langNames[this.currentLanguage] || 'EN';
  }
  getLanguageName(language) {
    const names = {
      'en': 'English',
      'es': 'Español',
      'zh': '中文'
    };
    return names[language] || 'English';
  }
  saveLanguagePreference() {
    localStorage.setItem('chatbot-language', this.currentLanguage);
  }
  loadLanguagePreference() {
    const savedLanguage = localStorage.getItem('chatbot-language');
    if (savedLanguage && ['en', 'es', 'zh'].includes(savedLanguage)) {
      this.currentLanguage = savedLanguage;
      this.updateLanguageSelector();
    }
  }
  getLanguageChangeMessage(language) {
    const messages = {
      'en': 'Language changed to English',
      'es': 'Idioma cambiado a Español',
      'zh': '语言已更改为中文'
    };
    return messages[language] || messages['en'];
  }
}
document.addEventListener('DOMContentLoaded', () => {
  window.chatbot = new AIChatbot();
});
