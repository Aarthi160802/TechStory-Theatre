/**
 * Main App Component
 * Orchestrates all screens and state management
 */

import React, { useEffect, useState } from 'react';
import { characterService, conversationService } from './services/api';
import { useAppStore } from './store/appStore';
import { ScenarioBuilder } from './screens/ScenarioBuilder';
import { SimulationView } from './screens/SimulationView';
import { ChatWithCharacter } from './screens/ChatWithCharacter';
import { PersonalityEditor } from './screens/PersonalityEditor';
import { ReplayWhatIf } from './screens/ReplayWhatIf';
import { LoadingSpinner, ErrorMessage } from './components';
import type { ConversationRequest, Character } from './types';
import './App.css';

function App() {
  const {
    currentScreen,
    currentConversation,
    setCurrentScreen,
    setCurrentConversation,
    setCharacters,
    setLoading,
    setError,
    clearError,
    characters,
    isLoading,
    error,
  } = useAppStore();

  const [characterOrder, setCharacterOrder] = useState<string[]>([]);
  const [chatCharacter, setChatCharacter] = useState<string | null>(null);

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
  }, [setCharacters, setError]);

  // =========== Scenario Builder Handlers ===========

  const handleStartConversation = async (
    scenario: string,
    characterNames: string[],
    order: string[]
  ) => {
    try {
      setLoading(true);
      setError(null);
      setCharacterOrder(order);

      // Create conversation request
      const request: ConversationRequest = {
        scenario,
        character_names: characterNames,
        turn_order: order,
        num_turns: order.length * 2, // 2 rounds
      };

      // Start conversation
      const response = await conversationService.start(request);

      // Fetch full conversation
      const fullConversation = await conversationService.get(response.conversation_id);

      setCurrentConversation({
        scenario: fullConversation.scenario,
        characters: fullConversation.characters?.flat ? 
          fullConversation.characters : 
          characters.filter(c => characterNames.includes(c.name)),
        messages: fullConversation.messages || [],
        created_at: fullConversation.created_at || new Date().toISOString(),
      });

      setCurrentScreen('simulation-view');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start conversation');
    } finally {
      setLoading(false);
    }
  };

  const handleNextTurn = async (nextSpeaker: string) => {
    if (!currentConversation) return;

    try {
      setLoading(true);
      // In a real implementation, this would call the backend
      // to generate the next response
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate response');
    }
  };

  const handleChatWithCharacter = (characterName: string) => {
    setChatCharacter(characterName);
    setCurrentScreen('chat');
  };

  const handleReplay = () => {
    setCurrentScreen('replay');
  };

  const handleBack = () => {
    setCurrentScreen('scenario-builder');
  };

  const handlePersonalityEditor = () => {
    setCurrentScreen('personality-editor');
  };

  const handleApplyPersonalityChanges = () => {
    setCurrentScreen('scenario-builder');
  };

  const handleReplayWithChanges = async (
    selectedChars: string[],
    turnOrder: string[],
    personalities: Record<string, any>
  ) => {
    if (!currentConversation) return;

    try {
      setLoading(true);
      setCharacterOrder(turnOrder);

      const request: ConversationRequest = {
        scenario: currentConversation.scenario,
        character_names: selectedChars,
        turn_order: turnOrder,
        num_turns: turnOrder.length * 2,
      };

      const response = await conversationService.start(request);
      const fullConversation = await conversationService.get(response.conversation_id);

      setCurrentConversation({
        scenario: fullConversation.scenario,
        characters: fullConversation.characters?.flat 
          ? fullConversation.characters 
          : characters.filter(c => selectedChars.includes(c.name)),
        messages: fullConversation.messages || [],
        created_at: fullConversation.created_at || new Date().toISOString(),
      });

      setCurrentScreen('simulation-view');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to replay scenario');
    } finally {
      setLoading(false);
    }
  };

  // =========== Render Current Screen ===========

  const renderCurrentScreen = () => {
    switch (currentScreen) {
      case 'scenario-builder':
        return (
          <ScenarioBuilder
            onStart={handleStartConversation}
            isLoading={isLoading}
          />
        );

      case 'simulation-view':
        return currentConversation ? (
          <SimulationView
            conversation={currentConversation}
            isLoading={isLoading}
            characterOrder={characterOrder}
            onNextTurn={handleNextTurn}
            onBack={handleBack}
            onChatWithCharacter={handleChatWithCharacter}
            onReplay={handleReplay}
          />
        ) : (
          <div>No conversation loaded</div>
        );

      case 'chat':
        return chatCharacter && currentConversation ? (
          <ChatWithCharacter
            characterName={chatCharacter}
            conversationId={currentConversation.created_at} // Using timestamp as ID
            scenario={currentConversation.scenario}
            onBack={handleBack}
          />
        ) : (
          <div>No character selected</div>
        );

      case 'personality-editor':
        return (
          <PersonalityEditor
            characters={characters}
            onApply={handleApplyPersonalityChanges}
            onBack={handleBack}
          />
        );

      case 'replay':
        return currentConversation ? (
          <ReplayWhatIf
            currentConversation={currentConversation}
            allCharacters={characters}
            onReplayWithChanges={handleReplayWithChanges}
            onBack={handleBack}
          />
        ) : (
          <div>No conversation to replay</div>
        );

      default:
        return <ScenarioBuilder onStart={handleStartConversation} isLoading={isLoading} />;
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🎭 Entertainment App</h1>
          <p>Watch AI characters interact and have epic conversations</p>
        </div>
        <nav className="header-nav">
          <button
            className={`nav-btn ${currentScreen === 'scenario-builder' ? 'active' : ''}`}
            onClick={() => setCurrentScreen('scenario-builder')}
          >
            Home
          </button>
          {currentScreen !== 'scenario-builder' && (
            <>
              <button
                className={`nav-btn ${currentScreen === 'personality-editor' ? 'active' : ''}`}
                onClick={handlePersonalityEditor}
              >
                Edit Personalities
              </button>
            </>
          )}
        </nav>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {isLoading && currentScreen === 'scenario-builder' && (
          <LoadingSpinner />
        )}

        {error && (
          <ErrorMessage message={error} onDismiss={clearError} />
        )}

        {renderCurrentScreen()}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Entertainment App © 2026 | Powered by AI Characters</p>
      </footer>
    </div>
  );
}

export default App;
