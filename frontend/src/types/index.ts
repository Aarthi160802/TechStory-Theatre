/**
 * Type definitions for Entertainment App
 */

export type PersonalityTrait = 
  | 'aggression' 
  | 'kindness' 
  | 'sarcasm' 
  | 'intelligence' 
  | 'humor';

export interface Character {
  name: string;
  base_system_prompt: string;
  personality_traits: Record<PersonalityTrait, number>;
  temperature: number;
  model_override?: string;
}

export interface Message {
  speaker_name: string;
  content: string;
  timestamp: string;
}

export interface ConversationLog {
  scenario: string;
  characters: Character[];
  messages: Message[];
  created_at: string;
  metadata?: Record<string, unknown>;
}

export interface PersonalityAdjustment {
  character_name: string;
  traits: Partial<Record<PersonalityTrait, number>>;
}

export interface ConversationRequest {
  scenario: string;
  character_names: string[];
  turn_order: string[];
  num_turns?: number;
  personality_adjustments?: PersonalityAdjustment[];
}

export interface ConversationResponse {
  conversation_id: string;
  scenario: string;
  messages: Message[];
  created_at: string;
}

export interface CharacterResponse {
  character_name: string;
  response: string;
}

export interface ApiError {
  error: string;
  status_code: number;
}

// Application state types
export interface AppState {
  currentScreen: 'scenario-builder' | 'simulation-view' | 'chat' | 'personality-editor' | 'replay';
  currentConversation: ConversationLog | null;
  characters: Character[];
  isLoading: boolean;
  error: string | null;
}
