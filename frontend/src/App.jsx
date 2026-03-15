import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [name, setName] = useState('');
  const [isSetupComplete, setIsSetupComplete] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSetupSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/set_name`, { name: name.trim() });
      setIsSetupComplete(true);
      setMessages([
        { id: 1, text: response.data.message, sender: 'bot' }
      ]);
    } catch (error) {
      console.error("Failed to set name", error);
      // Fallback for dev without backend
      setIsSetupComplete(true);
      setMessages([
        { id: 1, text: `Hi ${name.trim()}! Backend seems unreachable.`, sender: 'bot' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMsg = inputValue.trim();
    setInputValue('');
    
    // Add user message
    const tempId = Date.now();
    setMessages(prev => [...prev, { id: tempId, text: userMsg, sender: 'user' }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, { query: userMsg });
      setMessages(prev => [
        ...prev, 
        { id: Date.now() + 1, text: response.data.response, sender: 'bot' }
      ]);
    } catch (error) {
      console.error("Query failed", error);
      setMessages(prev => [
        ...prev, 
        { id: Date.now() + 1, text: "Error: Could not reach the server.", sender: 'bot' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isSetupComplete) {
    return (
      <div className="app-container fade-in">
        <div className="setup-screen">
          <h2>Welcome to Jarvis</h2>
          <p>Your personal AI assistant is ready.</p>
          <form className="setup-form" onSubmit={handleSetupSubmit}>
            <input 
              type="text" 
              placeholder="Enter your name" 
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={isLoading}
              autoFocus
            />
            <button type="submit" disabled={isLoading || !name.trim()}>
              {isLoading ? 'Connecting...' : 'Start Setup'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container fade-in">
      <div className="header">
        <div className="status"></div>
        <h1>Jarvis AI</h1>
      </div>
      
      <div className="chat-area">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="message bot" style={{ opacity: 0.7 }}>
            Typing...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-area" onSubmit={handleSendMessage}>
        <input 
          type="text" 
          placeholder="Ask Jarvis a question..." 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" disabled={!inputValue.trim() || isLoading}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}

export default App;
