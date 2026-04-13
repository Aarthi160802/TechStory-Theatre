/**
 * Reusable components for the Entertainment App
 */

import React from 'react';
import type { Message, Character } from '../types';
import './components.css';

// ==================== Conversation Display ====================

interface ConversationDisplayProps {
  messages: Message[];
  isLoading?: boolean;
  onScroll?: (e: React.UIEvent<HTMLDivElement>) => void;
}

export const ConversationDisplay: React.FC<ConversationDisplayProps> = ({
  messages,
  isLoading = false,
  onScroll,
}) => {
  React.useEffect(() => {
    // Auto-scroll to bottom
    const element = document.querySelector('.conversation-display');
    if (element) {
      element.scrollTop = element.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="conversation-display" onScroll={onScroll}>
      {messages.map((msg, idx) => (
        <div key={idx} className="message">
          <div className="message-speaker">{msg.speaker_name}</div>
          <div className="message-content">{msg.content}</div>
          <div className="message-time">
            {new Date(msg.timestamp).toLocaleTimeString()}
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="message loading">
          <div className="message-content">Generating response...</div>
        </div>
      )}
    </div>
  );
};

// ==================== Character Selector ====================

interface CharacterSelectorProps {
  characters: Character[];
  selectedCharacters: string[];
  onSelect: (characterNames: string[]) => void;
  multiSelect?: boolean;
}

export const CharacterSelector: React.FC<CharacterSelectorProps> = ({
  characters,
  selectedCharacters,
  onSelect,
  multiSelect = true,
}) => {
  const handleToggle = (name: string) => {
    if (multiSelect) {
      const newSelected = selectedCharacters.includes(name)
        ? selectedCharacters.filter((c) => c !== name)
        : [...selectedCharacters, name];
      onSelect(newSelected);
    } else {
      onSelect([name]);
    }
  };

  return (
    <div className="character-selector">
      <h3>Select Characters</h3>
      <div className="character-grid">
        {characters.map((char) => (
          <button
            key={char.name}
            className={`character-card ${
              selectedCharacters.includes(char.name) ? 'selected' : ''
            }`}
            onClick={() => handleToggle(char.name)}
          >
            <div className="character-name">{char.name}</div>
            <div className="character-traits">
              {Object.entries(char.personality_traits)
                .slice(0, 2)
                .map(([trait, value]) => (
                  <span key={trait} className="trait-badge">
                    {trait}: {value}
                  </span>
                ))}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

// ==================== Personality Slider ====================

interface PersonalitySliderProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
}

export const PersonalitySlider: React.FC<PersonalitySliderProps> = ({
  label,
  value,
  onChange,
  min = 0,
  max = 100,
}) => {
  return (
    <div className="personality-slider">
      <label>{label}</label>
      <div className="slider-container">
        <span className="slider-value">{min}</span>
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="slider-input"
        />
        <span className="slider-value">{max}</span>
      </div>
      <div className="slider-display">{value}</div>
    </div>
  );
};

// ==================== Loading Spinner ====================

export const LoadingSpinner: React.FC = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>Loading...</p>
  </div>
);

// ==================== Error Message ====================

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  onDismiss,
}) => (
  <div className="error-message">
    <div className="error-content">
      <span className="error-icon">⚠️</span>
      <span>{message}</span>
    </div>
    {onDismiss && (
      <button className="error-dismiss" onClick={onDismiss}>
        ×
      </button>
    )}
  </div>
);

// ==================== Button Variants ====================

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  disabled,
  className,
  ...props
}) => (
  <button
    className={`btn btn-${variant} btn-${size} ${className || ''}`}
    disabled={disabled || isLoading}
    {...props}
  >
    {isLoading ? '⏳ Loading...' : children}
  </button>
);
