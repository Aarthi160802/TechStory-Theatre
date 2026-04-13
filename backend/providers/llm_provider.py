"""LLM Provider abstraction layer for multiple language models."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
from enum import Enum


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Create a completion using the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2 for OpenAI, 0-1 typical)
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated text response
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI compatible provider (GPT-4, GPT-3.5, etc)."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4-turbo-preview)
        """
        from openai import OpenAI
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided and not in environment")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create completion using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or 500,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use (default: claude-3-sonnet-20240229)
        """
        from anthropic import Anthropic
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not provided and not in environment")
        
        self.model = model
        self.client = Anthropic(api_key=self.api_key)
    
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create completion using Anthropic API."""
        try:
            # Anthropic uses a different API structure
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or 500,
                messages=messages,
                temperature=temperature,
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")


class OllamaProvider(LLMProvider):
    """Local Ollama provider for running LLMs locally."""
    
    def __init__(self, base_url: Optional[str] = None, model: str = "mistral"):
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Ollama server URL (defaults to OLLAMA_BASE_URL or http://localhost:11434)
            model: Model to use (default: mistral)
        """
        import requests
        
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model
        self.requests = requests
    
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create completion using local Ollama."""
        try:
            # Format messages for Ollama
            prompt_text = ""
            for msg in messages:
                role = msg["role"].upper()
                content = msg["content"]
                prompt_text += f"{role}: {content}\n"
            
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt_text,
                    "temperature": temperature,
                    "stream": False,
                },
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")


class GoogleProvider(LLMProvider):
    """Google Gemini API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Google Gemini provider.
        
        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            model: Model to use (defaults to GOOGLE_MODEL env var or gemini-1.5-flash)
        """
        import google.generativeai as genai
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not provided and not in environment")
        
        # Read model from parameter, env var, or use fallback
        self.model = model or os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
    
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create completion using Google Gemini API."""
        try:
            # Format messages for Gemini
            prompt_text = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    prompt_text += f"System: {content}\n\n"
                elif role == "user":
                    prompt_text += f"User: {content}\n\n"
                else:
                    prompt_text += f"{role}: {content}\n\n"

            # Set a higher timeout (60 seconds)
            response = self.client.generate_content(
                prompt_text,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens or 500,
                },
                # If the SDK supports timeout, set it here; else, handle below
            )
            return response.text.strip()
        except Exception as e:
            # User-friendly error for timeouts
            if "Deadline expired before operation could complete" in str(e) or "504 Deadline expired" in str(e):
                raise RuntimeError("Google Gemini API timed out. Please try again with a shorter prompt or fewer turns.")
            raise RuntimeError(f"Google Gemini API error: {str(e)}")


class ProviderFactory:
    """Factory for creating LLM provider instances."""
    
    _providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
        "google": GoogleProvider,
    }
    
    @classmethod
    def create(cls, provider_name: Optional[str] = None, **kwargs) -> LLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_name: Name of provider (openai, anthropic, ollama)
                          Defaults to LLM_PROVIDER env var or 'openai'
            **kwargs: Additional arguments passed to provider constructor
        
        Returns:
            LLMProvider instance
        
        Raises:
            ValueError: If provider name is invalid
        """
        provider_name = provider_name or os.getenv("LLM_PROVIDER", "openai").lower()
        
        if provider_name not in cls._providers:
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available: {', '.join(cls._providers.keys())}"
            )
        
        provider_class = cls._providers[provider_name]
        return provider_class(**kwargs)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """Register a custom provider."""
        cls._providers[name.lower()] = provider_class
