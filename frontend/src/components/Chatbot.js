import React, { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId] = useState(uuidv4());
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { text: userMessage, sender: 'user', timestamp: new Date() }]);
    setIsTyping(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(prev => [...prev, { 
          text: data.response, 
          sender: 'bot', 
          timestamp: new Date() 
        }]);
      } else {
        const errorData = await response.json();
        setMessages(prev => [...prev, { 
          text: `Error: ${errorData.error || 'Failed to get response'}`, 
          sender: 'bot', 
          timestamp: new Date() 
        }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        text: 'Sorry, I\'m having trouble connecting right now. Please try again in a moment.', 
        sender: 'bot', 
        timestamp: new Date() 
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Chatbot Toggle Button */}
      <div className="chatbot-toggle" onClick={toggleChat}>
        <div className="chatbot-icon">
          {isOpen ? 'X' : 'AI'}
        </div>
        <span className="chatbot-label">
          {isOpen ? 'Close' : 'Assistant'}
        </span>
      </div>

      {/* Chatbot Interface */}
      {isOpen && (
        <div className="chatbot-container">
          {/* Chat Header */}
          <div className="chatbot-header">
            <div className="chatbot-title">
              <span className="chatbot-avatar">AI</span>
              <div>
                <h3>AI Pizza Assistant</h3>
                <span className="chatbot-status">Online</span>
              </div>
            </div>
            <div className="chatbot-controls">
              <button 
                className="chatbot-clear-btn"
                onClick={clearChat}
                title="Clear chat history"
              >
                Clear
              </button>
              <button 
                className="chatbot-close-btn"
                onClick={toggleChat}
                title="Close chat"
              >
                X
              </button>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="chatbot-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <p>Hello! I'm your AI Pizza Assistant. How can I help you today?</p>
                <p>Ask me about our pizzas, place an order, or get recommendations!</p>
              </div>
            )}
            
            {messages.map((message, index) => (
              <div 
                key={index} 
                className={`chatbot-message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
              >
                <div className="message-content">
                  {message.text}
                </div>
                <div className="message-time">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="chatbot-message bot-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="chatbot-input">
            <div className="input-container">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message here..."
                rows="1"
                disabled={isTyping}
              />
              <button 
                className="send-button"
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isTyping}
              >
                Send
              </button>
            </div>
            <div className="input-hint">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
