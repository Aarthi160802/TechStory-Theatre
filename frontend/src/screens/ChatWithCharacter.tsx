/**
 * Screen 3: Chat with Character
 * User talks to a character about the scenario
 */

import React, { useRef, useEffect, useState } from 'react';
import { chatService } from '../services/api';
import { Button, ErrorMessage } from '../components';
import type { Message } from '../types';
import './screens.css';

interface ChatWithCharacterProps {
  characterName: string;
  conversationId: string;
  scenario: string;
  onBack: () => void;
}

export const ChatWithCharacter: React.FC<ChatWithCharacterProps> = ({
  characterName,
  conversationId,
  scenario,
  onBack,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messageEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message
      const userMessage: Message = {
        speaker_name: 'You',
        content: input,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Get character response
      const response = await chatService.send(
        characterName,
        conversationId,
        input
      );

      const charMessage: Message = {
        speaker_name: characterName,
        content: response.response,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, charMessage]);

      setInput('');
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to get response'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="screen chat-with-character">
      <div className="screen-header">
        <div className="header-left">
          <h1>💬 Chat with {characterName}</h1>
          <p className="scenario-context">
            Discussing: "{scenario}"
          </p>
        </div>
        <Button variant="secondary" size="md" onClick={onBack}>
          ← Back
        </Button>
      </div>

      <div className="screen-content chat-content">
        {error && (
          <ErrorMessage message={error} onDismiss={() => setError(null)} />
        )}

        {/* Messages */}
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-empty">
              <p>Start a conversation with {characterName}!</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${
                msg.speaker_name === 'You' ? 'user-message' : 'character-message'
              }`}
            >
              <div className="message-speaker">{msg.speaker_name}</div>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}
          {isLoading && (
            <div className="chat-message character-message loading">
              <div className="message-content">Thinking...</div>
            </div>
          )}
          <div ref={messageEndRef} />
        </div>

        {/* Input */}
        <div className="chat-input-area">
          <div className="input-row">
            <input
              type="text"
              className="chat-input"
              placeholder={`Say something to ${characterName}...`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !isLoading) {
                  handleSendMessage();
                }
              }}
              disabled={isLoading}
            />
            <Button
              variant="primary"
              size="md"
              onClick={handleSendMessage}
              isLoading={isLoading}
              disabled={!input.trim()}
            >
              Send
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
