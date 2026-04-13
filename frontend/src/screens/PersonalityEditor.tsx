/**
 * Screen 4: Personality Editor
 * User adjusts personality traits for characters
 */

import React, { useState } from 'react';
import { useAppStore } from '../store/appStore';
import { PersonalitySlider, Button } from '../components';
import type { Character, PersonalityTrait } from '../types';
import './screens.css';

const PERSONALITY_TRAITS: PersonalityTrait[] = [
  'aggression',
  'kindness',
  'sarcasm',
  'intelligence',
  'humor',
];

interface PersonalityEditorProps {
  characters: Character[];
  onApply: () => void;
  onBack: () => void;
}

export const PersonalityEditor: React.FC<PersonalityEditorProps> = ({
  characters,
  onApply,
  onBack,
}) => {
  const { personalityAdjustments, setPersonalityAdjustments } = useAppStore();
  const [editingCharacter, setEditingCharacter] = useState<string>(
    characters[0]?.name || ''
  );

  const currentCharacter = characters.find((c) => c.name === editingCharacter);
  const currentAdjustments =
    personalityAdjustments[editingCharacter]?.traits || {};

  const handleTraitChange = (trait: PersonalityTrait, value: number) => {
    const newAdjustments = {
      character_name: editingCharacter,
      traits: {
        ...currentAdjustments,
        [trait]: value,
      },
    };
    setPersonalityAdjustments(editingCharacter, newAdjustments);
  };

  const handleReset = () => {
    const newAdjustments = {
      character_name: editingCharacter,
      traits: {},
    };
    setPersonalityAdjustments(editingCharacter, newAdjustments);
  };

  if (!currentCharacter) {
    return <div className="screen">No characters available</div>;
  }

  return (
    <div className="screen personality-editor">
      <div className="screen-header">
        <h1>🎚️ Personality Editor</h1>
        <p>Adjust traits to customize character behavior</p>
      </div>

      <div className="screen-content editor-content">
        {/* Character Selector */}
        <div className="editor-sidebar">
          <h3>Characters</h3>
          <div className="character-list">
            {characters.map((char) => (
              <button
                key={char.name}
                className={`character-btn ${
                  editingCharacter === char.name ? 'active' : ''
                }`}
                onClick={() => setEditingCharacter(char.name)}
              >
                {char.name}
              </button>
            ))}
          </div>
        </div>

        {/* Editor Panel */}
        <div className="editor-main">
          <div className="editor-header">
            <h2>{editingCharacter}</h2>
            <Button variant="secondary" size="sm" onClick={handleReset}>
              Reset to Default
            </Button>
          </div>

          {/* Original Traits Display */}
          <div className="trait-section original">
            <h4>Default Traits</h4>
            <div className="traits-display">
              {PERSONALITY_TRAITS.map((trait) => (
                <div key={trait} className="trait-item">
                  <span className="trait-name">{trait}</span>
                  <div className="trait-bar">
                    <div
                      className="trait-fill"
                      style={{
                        width: `${currentCharacter.personality_traits[trait]}%`,
                      }}
                    />
                  </div>
                  <span className="trait-value">
                    {currentCharacter.personality_traits[trait]}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Adjustment Sliders */}
          <div className="trait-section adjustments">
            <h4>Adjust Traits</h4>
            {PERSONALITY_TRAITS.map((trait) => (
              <PersonalitySlider
                key={trait}
                label={trait.charAt(0).toUpperCase() + trait.slice(1)}
                value={
                  currentAdjustments[trait] ||
                  currentCharacter.personality_traits[trait]
                }
                onChange={(value) => handleTraitChange(trait, value)}
              />
            ))}
          </div>

          {/* Adjusted Preview */}
          <div className="trait-section preview">
            <h4>Adjusted Traits Preview</h4>
            <div className="traits-display">
              {PERSONALITY_TRAITS.map((trait) => (
                <div key={trait} className="trait-item">
                  <span className="trait-name">{trait}</span>
                  <div className="trait-bar">
                    <div
                      className="trait-fill adjusted"
                      style={{
                        width: `${
                          currentAdjustments[trait] ||
                          currentCharacter.personality_traits[trait]
                        }%`,
                      }}
                    />
                  </div>
                  <span className="trait-value">
                    {currentAdjustments[trait] ||
                      currentCharacter.personality_traits[trait]}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="screen-actions">
        <Button variant="primary" size="lg" onClick={onApply}>
          ✓ Apply Changes
        </Button>
        <Button variant="secondary" size="lg" onClick={onBack}>
          ← Back
        </Button>
      </div>
    </div>
  );
};
