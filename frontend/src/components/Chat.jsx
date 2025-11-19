import { useState, useEffect } from 'react';
import { uploadPDF, sendMessage } from '../api';
import { useNavigate } from 'react-router-dom';

function Chat() {
  const [sessionId, setSessionId] = useState(localStorage.getItem('current_session_id') || '');
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('chat_messages');
    return saved ? JSON.parse(saved) : [];
  });
  const [input, setInput] = useState('');
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('current_session_id', sessionId);
    }
  }, [sessionId]);

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chat_messages', JSON.stringify(messages));
    }
  }, [messages]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setUploading(true);
    try {
      const response = await uploadPDF(file);
      setSessionId(response.data.session_id);
      setMessages([{
        type: 'system',
        content: `PDF "${response.data.filename}" uploaded successfully! You can now ask questions about it.`
      }]);
    } catch (err) {
      if (err.response?.status === 401) {
        navigate('/login');
      } else {
        alert('Upload failed: ' + (err.response?.data?.detail || 'Unknown error'));
      }
    } finally {
      setUploading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;
    
    const userMessage = input;
    setMessages([...messages, { type: 'user', content: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const response = await sendMessage(userMessage, sessionId);
      setMessages((prev) => [...prev, {
        type: 'assistant',
        content: response.data.answer,
        sources: response.data.sources
      }]);
    } catch (err) {
      if (err.response?.status === 401) {
        navigate('/login');
      } else {
        setMessages((prev) => [...prev, {
          type: 'error',
          content: 'Failed to get response: ' + (err.response?.data?.detail || 'Unknown error')
        }]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('current_session_id');
    localStorage.removeItem('chat_messages');
    navigate('/login');
  };

  const handleNewChat = () => {
    setSessionId('');
    setMessages([]);
    setFile(null);
    localStorage.removeItem('current_session_id');
    localStorage.removeItem('chat_messages');
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>PDF Chat</h2>
        <div>
          {sessionId && (
            <button onClick={handleNewChat} className="new-chat-btn">New Chat</button>
          )}
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </div>

      <div className="upload-section">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          disabled={uploading || sessionId}
        />
        <button
          onClick={handleUpload}
          disabled={!file || uploading || sessionId}
        >
          {uploading ? 'Uploading...' : sessionId ? 'PDF Uploaded' : 'Upload PDF'}
        </button>
      </div>

      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <div className="message-content">{msg.content}</div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                {msg.sources.map((source, i) => (
                  <div key={i} className="source">{source}</div>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="message loading">Thinking...</div>}
      </div>

      <div className="input-section">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder={sessionId ? "Ask a question about the PDF..." : "Upload a PDF first"}
          disabled={!sessionId || loading}
        />
        <button onClick={handleSend} disabled={!sessionId || !input.trim() || loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;
