/**
 * Screen 2: Simulation View
 * Shows live conversation with speaker selection and controls
 */

import React, { useState } from 'react';
import { useAppStore } from '../store/appStore';
import { ConversationDisplay, Button } from '../components';
import type { ConversationLog } from '../types';
import './screens.css';

interface SimulationViewProps {
  conversation: ConversationLog;
  isLoading: boolean;
  characterOrder: string[];
  onNextTurn: (nextSpeaker: string) => void;
  onBack: () => void;
  onChatWithCharacter: (characterName: string) => void;
  onReplay: () => void;
}

export const SimulationView: React.FC<SimulationViewProps> = ({
  conversation,
  isLoading,
  characterOrder,
  onNextTurn,
  onBack,
  onChatWithCharacter,
  onReplay,
}) => {
  const [playSpeed, setPlaySpeed] = useState(1);
  const [showControls, setShowControls] = useState(true);

  // Determine next speaker (cycle through turn order)
  const nextSpeakerIdx =
    (conversation.messages.length % characterOrder.length);
  const nextSpeaker = characterOrder[nextSpeakerIdx];

  const upcomingSpeakers = characterOrder.slice(nextSpeakerIdx);

  return (
    <div className="screen simulation-view">
      <div className="screen-header">
        <div className="header-left">
          <h1>🎬 Live Simulation</h1>
          <p className="scenario-display">
            <strong>Scenario:</strong> {conversation.scenario}
          </p>
        </div>
        <div className="header-stats">
          <span className="stat">
            <strong>Messages:</strong> {conversation.messages.length}
          </span>
          <span className="stat">
            <strong>Characters:</strong> {conversation.characters.length}
          </span>
        </div>
      </div>

      <div className="screen-content simulation-content">
        {/* Main Conversation Display */}
        <div className="conversation-section">
          <ConversationDisplay messages={conversation.messages} isLoading={isLoading} />
        </div>

        {/* Control Panel */}
        <div className="control-panel">
          <div className="controls-toggle">
            <button
              className="toggle-btn"
              onClick={() => setShowControls(!showControls)}
            >
              {showControls ? '▼ Hide' : '▶ Show'} Controls
            </button>
          </div>

          {showControls && (
            <div className="controls-expanded">
              {/* Next Speaker Section */}
              <div className="control-section">
                <h3>Next Speaker</h3>
                <div className="next-speaker">
                  <span className="speaker-badge">{nextSpeaker}</span>
                  {isLoading ? (
                    <span className="generating-badge">🔄 Generating...</span>
                  ) : (
                    <Button
                      variant="primary"
                      size="md"
                      onClick={() => onNextTurn(nextSpeaker)}
                    >
                      Next Turn →
                    </Button>
                  )}
                </div>
              </div>

              {/* Queue Preview */}
              <div className="control-section">
                <h3>Speaker Queue</h3>
                <div className="speaker-queue">
                  {upcomingSpeakers.map((speaker, idx) => (
                    <div key={idx} className="queue-item">
                      <span className="queue-number">{idx + 1}</span>
                      <span className="queue-name">{speaker}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Playback Speed */}
              <div className="control-section">
                <h3>Speed</h3>
                <div className="speed-control">
                  <input
                    type="range"
                    min="0.5"
                    max="2"
                    step="0.25"
                    value={playSpeed}
                    onChange={(e) => setPlaySpeed(Number(e.target.value))}
                    className="speed-slider"
                  />
                  <span className="speed-value">{playSpeed}x</span>
                </div>
              </div>

              {/* Character Interaction Shortcuts */}
              <div className="control-section">
                <h3>Talk to Character</h3>
                <div className="character-shortcuts">
                  {conversation.characters.map((char) => (
                    <Button
                      key={char.name}
                      variant="secondary"
                      size="sm"
                      onClick={() => onChatWithCharacter(char.name)}
                    >
                      💬 {char.name}
                    </Button>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="control-section actions">
                <Button
                  variant="secondary"
                  size="md"
                  onClick={onReplay}
                >
                  🔁 Replay
                </Button>
                <Button variant="default" size="md" onClick={onBack}>
                  ← Back
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
