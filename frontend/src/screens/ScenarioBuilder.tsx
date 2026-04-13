/**
 * Screen 1: Scenario Builder
 * User inputs scenario, selects characters, and starts simulation
 */

import React, { useState, useEffect } from 'react';
import { characterService } from '../services/api';
import { useAppStore } from '../store/appStore';
import { CharacterSelector, Button, ErrorMessage } from '../components';
import type { Character } from '../types';
import './screens.css';

interface ScenarioBuilderProps {
  onStart: (scenario: string, characters: string[], order: string[]) => void;
  isLoading: boolean;
}

export const ScenarioBuilder: React.FC<ScenarioBuilderProps> = ({
  onStart,
  isLoading,
}) => {
  const [scenario, setScenario] = useState(
    'Project deadline is tomorrow but work is incomplete.'
  );
  const [characters, setCharacters] = useState<Character[]>([]);
  const [selectedCharacters, setSelectedCharacters] = useState<string[]>([
    'Strict Boss',
    'Lazy Lead',
    'Gen Z Intern',
  ]);
  const [turnOrder, setTurnOrder] = useState<string[]>([
    'Strict Boss',
    'Lazy Lead',
    'Gen Z Intern',
  ]);
  const [numTurns, setNumTurns] = useState(12);
  const [error, setError] = useState<string | null>(null);
  const { clearError } = useAppStore();

  // Load characters on mount
  useEffect(() => {
    const loadCharacters = async () => {
      try {
        const result = await characterService.getAll();
        setCharacters(result.characters);
      } catch (err) {
        setError('Failed to load characters');
      }
    };
    loadCharacters();
  }, []);

  const handleCharacterSelect = (selected: string[]) => {
    setSelectedCharacters(selected);
    // Reset turn order if needed
    if (selected.length > 0 && turnOrder.length === 0) {
      setTurnOrder([selected[0]]);
    }
  };

  const handleAddToTurnOrder = (character: string) => {
    if (!turnOrder.includes(character)) {
      setTurnOrder([...turnOrder, character]);
    }
  };

  const handleRemoveFromTurnOrder = (index: number) => {
    setTurnOrder(turnOrder.filter((_, i) => i !== index));
  };

  const handleStart = () => {
    if (!scenario.trim()) {
      setError('Please enter a scenario');
      return;
    }
    if (selectedCharacters.length === 0) {
      setError('Please select at least one character');
      return;
    }
    if (turnOrder.length === 0) {
      setError('Please set up the turn order');
      return;
    }
    clearError();
    onStart(scenario, selectedCharacters, turnOrder);
  };

  return (
    <div className="screen scenario-builder">
      <div className="screen-header">
        <h1>🎭 Create Your Scene</h1>
        <p>Set up a scenario and watch characters interact</p>
      </div>

      <div className="screen-content">
        {error && (
          <ErrorMessage
            message={error}
            onDismiss={() => setError(null)}
          />
        )}

        {/* Scenario Input */}
        <div className="scenario-section">
          <h2>📝 Scenario Description</h2>
          <textarea
            className="scenario-input"
            placeholder="Describe the scenario (e.g., 'Project deadline is tomorrow but work is incomplete')"
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            rows={4}
          />
          <div className="input-hint">
            Be specific: The characters will respond better to detailed scenarios
          </div>
        </div>

        {/* Character Selection */}
        <div className="characters-section">
          <CharacterSelector
            characters={characters}
            selectedCharacters={selectedCharacters}
            onSelect={handleCharacterSelect}
            multiSelect={true}
          />
        </div>

        {/* Turn Order Setup */}
        <div className="turnorder-section">
          <h3>🎬 Set Turn Order</h3>
          <p className="section-hint">Click characters below to set who speaks and in what order</p>
          
          <div className="turn-order-display">
            {turnOrder.length > 0 ? (
              turnOrder.map((name, idx) => (
                <div key={idx} className="turn-item">
                  <span className="turn-number">{idx + 1}</span>
                  <span className="turn-name">{name}</span>
                  <button
                    className="turn-remove"
                    onClick={() => handleRemoveFromTurnOrder(idx)}
                  >
                    ×
                  </button>
                </div>
              ))
            ) : (
              <div className="turn-empty">Select characters to set turn order</div>
            )}
          </div>

          <div className="turn-add-options">
            {selectedCharacters.map((char) => (
              <button
                key={char}
                className={`turn-add-btn ${turnOrder.includes(char) ? 'in-order' : ''}`}
                onClick={() => handleAddToTurnOrder(char)}
              >
                + {char}
              </button>
            ))}
          </div>
        </div>

        {/* Number of Turns */}
        <div className="turns-section">
          <label>Number of Turns: {numTurns}</label>
          <input
            type="range"
            min="4"
            max="30"
            value={numTurns}
            onChange={(e) => setNumTurns(Number(e.target.value))}
            className="turns-slider"
          />
          <div className="turns-hint">
            Each selected character speaks once per round
          </div>
        </div>

        {/* Start Button */}
        <div className="action-section">
          <Button
            variant="primary"
            size="lg"
            onClick={handleStart}
            isLoading={isLoading}
            className="start-btn"
          >
            ▶️ Start Simulation
          </Button>
        </div>
      </div>
    </div>
  );
};
