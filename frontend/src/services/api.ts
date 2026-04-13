/**
 * API Service Layer
 * Handles all communication with backend
 */

import axios from 'axios';
import type {
  Character,
  ConversationRequest,
  ConversationResponse,
  CharacterResponse,
  ApiError,
} from '../types';

const API_BASE_URL = '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handler
const handleError = (error: unknown): ApiError => {
  if (axios.isAxiosError(error)) {
    return {
      error: error.response?.data?.error || error.message,
      status_code: error.response?.status || 500,
    };
  }
  return {
    error: String(error),
    status_code: 500,
  };
};

// Character endpoints
export const characterService = {
  getAll: async (): Promise<{ characters: Character[] }> => {
    try {
      const response = await apiClient.get('/characters');
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  getByName: async (name: string): Promise<Character> => {
    try {
      const response = await apiClient.get(`/characters/${name}`);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },
};

// Conversation endpoints
export const conversationService = {
  start: async (request: ConversationRequest): Promise<ConversationResponse> => {
    try {
      const response = await apiClient.post('/conversations/run', request);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  get: async (conversationId: string): Promise<ConversationResponse> => {
    try {
      const response = await apiClient.get(`/conversations/${conversationId}`);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },
};

// Chat endpoints
export const chatService = {
  send: async (
    characterName: string,
    conversationId: string,
    message: string,
  ): Promise<CharacterResponse> => {
    try {
      const response = await apiClient.post(
        `/chat/${characterName}`,
        {
          character_name: characterName,
          content: message,
        },
        {
          params: { conversation_id: conversationId },
        },
      );
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },
};

// Health check
export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/health');
    return response.status === 200;
  } catch {
    return false;
  }
};

export default apiClient;
