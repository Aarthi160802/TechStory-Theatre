"""Core conversation engine for character interactions."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from models.character import Character
from providers.llm_provider import ProviderFactory, LLMProvider


@dataclass
class Message:
    """Represents a single message in a conversation."""
    
    speaker_name: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "speaker_name": self.speaker_name,
            "content": self.content,
            "timestamp": self.timestamp,
        }


@dataclass
class ConversationLog:
    """Represents a full conversation history."""
    
    scenario: str
    characters: List[Character]
    messages: List[Message] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, speaker_name: str, content: str) -> None:
        """Add a message to the conversation log."""
        self.messages.append(Message(speaker_name=speaker_name, content=content))
    
    def get_conversation_text(self) -> str:
        """Get full conversation as formatted text."""
        text = f"Scenario: {self.scenario}\n\n"
        for msg in self.messages:
            text += f"{msg.speaker_name}: {msg.content}\n\n"
        return text
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "scenario": self.scenario,
            "characters": [c.to_dict() for c in self.characters],
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


class ConversationManager:
    """
    Manages multi-character conversations with memory and turn-taking logic.
    
    Handles:
    - Conversation history tracking
    - Character memory (context from previous messages)
    - Turn-based interaction
    - LLM provider abstraction
    """
    
    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        max_conversation_memory: int = 10,
    ):
        """
        Initialize ConversationManager.
        
        Args:
            llm_provider: LLM provider instance (defaults to factory-created)
            max_conversation_memory: Number of previous messages to include in context
        """
        self.llm_provider = llm_provider or ProviderFactory.create()
        self.max_conversation_memory = max_conversation_memory
    
    def run_turns(
        self,
        scenario: str,
        characters: List[Character],
        turn_order: List[str],  # Character names in order of who speaks
        num_turns: Optional[int] = None,
    ) -> ConversationLog:
        """
        Run a conversation with specified turn order.
        
        Args:
            scenario: The scenario description
            characters: List of Character objects
            turn_order: List of character names specifying turn order
                       (cycles through if num_turns exceeds length)
            num_turns: Number of turns to run (defaults to len(turn_order))
        
        Returns:
            ConversationLog with full conversation history
        """
        if num_turns is None:
            num_turns = len(turn_order)
        
        # Create character lookup
        char_dict = {char.name: char for char in characters}
        
        # Validate turn order
        for name in turn_order:
            if name not in char_dict:
                raise ValueError(f"Character '{name}' not found in character list")
        
        # Initialize conversation log
        log = ConversationLog(scenario=scenario, characters=characters)
        
        # Run conversation turns
        for turn_idx in range(num_turns):
            speaker_idx = turn_idx % len(turn_order)
            speaker_name = turn_order[speaker_idx]
            speaker = char_dict[speaker_name]
            
            # Generate response
            response = self._get_character_response(
                speaker=speaker,
                scenario=scenario,
                conversation_log=log,
            )
            
            # Add to log
            log.add_message(speaker_name, response)
            print(f"[Turn {turn_idx + 1}] {speaker_name}: {response}")
        
        return log
    
    def _get_character_response(
        self,
        speaker: Character,
        scenario: str,
        conversation_log: ConversationLog,
    ) -> str:
        """
        Generate a response from a character.
        
        Builds context from current conversation and scenarios,
        then queries LLM with character's system prompt.
        
        Args:
            speaker: The character generating response
            scenario: Current scenario description
            conversation_log: The conversation history
        
        Returns:
            Generated response text
        """
        # Build conversation context (recent messages only)
        context_messages = conversation_log.messages[-self.max_conversation_memory :]
        conversation_text = ""
        for msg in context_messages:
            conversation_text += f"{msg.speaker_name}: {msg.content}\n"
        
        # Build user prompt with context
        user_content = f"""Scenario: {scenario}

Current conversation:
{conversation_text}

Now respond as {speaker.name}. Keep your response to 1-2 sentences, natural and in character."""
        
        # Prepare messages for LLM
        messages = [
            {
                "role": "system",
                "content": speaker.get_adjusted_prompt(),
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]
        
        # Get response from LLM
        response = self.llm_provider.create_completion(
            messages=messages,
            temperature=speaker.temperature,
            max_tokens=150,
        )
        
        return response
    
    def add_user_message(
        self,
        conversation_log: ConversationLog,
        user_name: str,
        message_text: str,
    ) -> None:
        """Add a user message to conversation log."""
        conversation_log.add_message(user_name, message_text)
    
    def generate_character_response_in_context(
        self,
        character: Character,
        conversation_log: ConversationLog,
    ) -> str:
        """
        Generate a character response within the context of a conversation.
        
        Useful for "Talk to Character" feature where user chats with a character
        about a specific scenario/conversation.
        
        Args:
            character: The character replying
            conversation_log: The conversation they're responding in
        
        Returns:
            Character's response
        """
        # Include full conversation context
        conversation_text = conversation_log.get_conversation_text()
        
        # Get last few messages to understand context
        recent_messages = conversation_log.messages[-3:]
        recent_text = "\n".join(
            [f"{m.speaker_name}: {m.content}" for m in recent_messages]
        )
        
        user_content = f"""You are participating in this conversation:

{conversation_text}

Based on the recent messages:
{recent_text}

Respond as {character.name}. Keep your response to 1-2 sentences."""
        
        messages = [
            {
                "role": "system",
                "content": character.get_adjusted_prompt(),
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]
        
        return self.llm_provider.create_completion(
            messages=messages,
            temperature=character.temperature,
            max_tokens=150,
        )
