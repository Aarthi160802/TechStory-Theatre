/**
 * Zustand store for application state management
 */

import { create } from 'zustand';
import type {
  AppState,
  Character,
  ConversationLog,
  PersonalityAdjustment,
} from '../types';

interface AppStore extends AppState {
  // Actions
  setCurrentScreen: (screen: AppState['currentScreen']) => void;
  setCurrentConversation: (conversation: ConversationLog | null) => void;
  setCharacters: (characters: Character[]) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;

  // Personality management
  personalityAdjustments: Record<string, PersonalityAdjustment>;
  setPersonalityAdjustments: (char: string, adjustment: PersonalityAdjustment) => void;
  resetPersonalityAdjustments: () => void;

  // Recent conversations
  conversations: ConversationLog[];
  addConversation: (conversation: ConversationLog) => void;
  clearConversations: () => void;
}

export const useAppStore = create<AppStore>((set) => ({
  // Initial state
  currentScreen: 'scenario-builder',
  currentConversation: null,
  characters: [],
  isLoading: false,
  error: null,
  personalityAdjustments: {},
  conversations: [],

  // Screen actions
  setCurrentScreen: (screen) =>
    set({ currentScreen: screen }),

  setCurrentConversation: (conversation) =>
    set({ currentConversation: conversation }),

  setCharacters: (characters) =>
    set({ characters }),

  setLoading: (isLoading) =>
    set({ isLoading }),

  setError: (error) =>
    set({ error }),

  clearError: () =>
    set({ error: null }),

  // Personality management
  setPersonalityAdjustments: (char, adjustment) =>
    set((state) => ({
      personalityAdjustments: {
        ...state.personalityAdjustments,
        [char]: adjustment,
      },
    })),

  resetPersonalityAdjustments: () =>
    set({ personalityAdjustments: {} }),

  // Conversation history
  addConversation: (conversation) =>
    set((state) => ({
      conversations: [conversation, ...state.conversations].slice(0, 20), // Keep last 20
    })),

  clearConversations: () =>
    set({ conversations: [] }),
}));
