/**
 * Screen 5: Replay / What-If
 * User can reload past scenarios and modify parameters
 */

import React, { useState, useEffect } from 'react';
import { useAppStore } from '../store/appStore';
import { Button, CharacterSelector } from '../components';
import type { ConversationLog, Character } from '../types';
import './screens.css';

interface ReplayWhatIfProps {
  currentConversation: ConversationLog;
  allCharacters: Character[];
  onReplayWithChanges: (
    selectedChars: string[],
    turnOrder: string[],
    personalities: Record<string, any>
  ) => void;
  onBack: () => void;
}

export const ReplayWhatIf: React.FC<ReplayWhatIfProps> = ({
  currentConversation,
  allCharacters,
  onReplayWithChanges,
  onBack,
}) => {
  const { conversations } = useAppStore();
  const [selectedScenario, setSelectedScenario] = useState(
    currentConversation.scenario
  );
  const [selectedCharacters, setSelectedCharacters] = useState(
    currentConversation.characters.map((c) => c.name)
  );
  const [turnOrder, setTurnOrder] = useState(
    currentConversation.characters.map((c) => c.name)
  );
  const [modifiedTraits, setModifiedTraits] = useState<Record<string, any>>({});

  const handleAddToOrder = (char: string) => {
    if (!turnOrder.includes(char)) {
      setTurnOrder([...turnOrder, char]);
    }
  };

  const handleRemoveFromOrder = (idx: number) => {
    setTurnOrder(turnOrder.filter((_, i) => i !== idx));
  };

  const handleReplay = () => {
    onReplayWithChanges(selectedCharacters, turnOrder, modifiedTraits);
  };

  return (
    <div className="screen replay-whatif">
      <div className="screen-header">
        <h1>🔁 Replay / What-If</h1>
        <p>Modify and re-run your scenario</p>
      </div>

      <div className="screen-content replay-content">
        <div className="replay-grid">
          {/* Left Panel: Scenario & History */}
          <div className="replay-panel">
            <h3>Scenario</h3>
            <div className="scenario-display">
              <p>{selectedScenario}</p>
            </div>

            {conversations.length > 0 && (
              <>
                <h3>Past Scenarios</h3>
                <div className="scenario-history">
                  {conversations.slice(0, 5).map((conv, idx) => (
                    <button
                      key={idx}
                      className={`scenario-item ${
                        conv.scenario === selectedScenario ? 'active' : ''
                      }`}
                      onClick={() => setSelectedScenario(conv.scenario)}
                    >
                      <div className="scenario-preview">
                        {conv.scenario.substring(0, 50)}...
                      </div>
                      <div className="scenario-meta">
                        {conv.messages.length} messages
                      </div>
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Right Panel: Character Setup */}
          <div className="replay-panel">
            <h3>Characters & Turn Order</h3>

            <CharacterSelector
              characters={allCharacters}
              selectedCharacters={selectedCharacters}
              onSelect={setSelectedCharacters}
            />

            <h4 style={{ marginTop: '20px' }}>Turn Order</h4>
            <div className="turn-order-replay">
              {turnOrder.map((name, idx) => (
                <div key={idx} className="turn-item-replay">
                  <span className="turn-num">{idx + 1}</span>
                  <span className="turn-text">{name}</span>
                  <button
                    className="turn-remove-btn"
                    onClick={() => handleRemoveFromOrder(idx)}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>

            <div className="add-to-order-buttons">
              {selectedCharacters.map((char) => (
                <Button
                  key={char}
                  variant="secondary"
                  size="sm"
                  onClick={() => handleAddToOrder(char)}
                >
                  + {char}
                </Button>
              ))}
            </div>
          </div>
        </div>

        {/* Replay Summary */}
        <div className="replay-summary">
          <h3>📊 Replay Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="label">Characters:</span>
              <span className="value">{selectedCharacters.length}</span>
            </div>
            <div className="summary-item">
              <span className="label">Turn Order Length:</span>
              <span className="value">{turnOrder.length}</span>
            </div>
            <div className="summary-item">
              <span className="label">Personality Mods:</span>
              <span className="value">{Object.keys(modifiedTraits).length}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="screen-actions">
        <Button
          variant="primary"
          size="lg"
          onClick={handleReplay}
          disabled={selectedCharacters.length === 0 || turnOrder.length === 0}
        >
          ▶️ Run Replay
        </Button>
        <Button variant="secondary" size="lg" onClick={onBack}>
          ← Back
        </Button>
      </div>
    </div>
  );
};
