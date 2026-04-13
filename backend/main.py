"""FastAPI application for Entertainment App backend."""

import json
import os
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from models.character import Character, PersonalityTrait
from engines.conversation import ConversationManager, ConversationLog
from providers.llm_provider import ProviderFactory

# Initialize FastAPI app
app = FastAPI(
    title="Entertainment App API",
    description="LLM-powered character interaction engine",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models for API
# ============================================================================


class PersonalityAdjustment(BaseModel):
    """Adjustment to a character's personality traits."""
    
    character_name: str
    traits: Dict[str, int]  # e.g. {"aggression": 80, "kindness": 30}


class ConversationRequest(BaseModel):
    """Request to start a conversation."""
    
    scenario: str
    character_names: List[str]
    turn_order: List[str]
    num_turns: Optional[int] = None
    personality_adjustments: Optional[List[PersonalityAdjustment]] = None


class ChatMessage(BaseModel):
    """A chat message."""
    
    character_name: str
    content: str


class CharacterResponse(BaseModel):
    """Response containing a character's message."""
    
    character_name: str
    content: str


# ============================================================================
# Global State
# ============================================================================

# Load character definitions
def load_characters() -> Dict[str, Character]:
    """Load character definitions from config file."""
    config_path = os.path.join(
        os.path.dirname(__file__), "config", "characters.json"
    )
    with open(config_path, "r") as f:
        config = json.load(f)
    
    characters = {}
    for char_data in config["characters"]:
        char = Character.from_dict(char_data)
        characters[char.name] = char
    
    return characters


CHARACTERS = load_characters()
CONVERSATION_MANAGER = ConversationManager()
CONVERSATIONS: Dict[str, ConversationLog] = {}  # In-memory storage


# ============================================================================
# Utility Functions
# ============================================================================


def apply_personality_adjustments(
    character: Character,
    adjustments: Optional[List[PersonalityAdjustment]],
) -> Character:
    """Apply personality adjustments to a character."""
    if not adjustments:
        return character
    
    # Find adjustments for this character
    for adj in adjustments:
        if adj.character_name == character.name:
            # Create new character with adjusted traits
            new_traits = character.personality_traits.copy()
            for trait_name, value in adj.traits.items():
                try:
                    trait = PersonalityTrait(trait_name)
                    new_traits[trait] = value
                except ValueError:
                    pass  # Skip unknown traits
            
            # Return new character instance with adjusted traits
            return Character(
                name=character.name,
                base_system_prompt=character.base_system_prompt,
                personality_traits=new_traits,
                model_override=character.model_override,
                temperature=character.temperature,
            )
    
    return character


# ============================================================================
# API Endpoints
# ============================================================================


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Entertainment App API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/characters")
async def get_characters():
    """Get all available characters."""
    return {
        "characters": [
            {
                "name": name,
                "base_prompt_preview": char.base_system_prompt[:100] + "...",
                "personality_traits": {
                    k.value: v for k, v in char.personality_traits.items()
                },
            }
            for name, char in CHARACTERS.items()
        ]
    }


@app.get("/api/characters/{character_name}")
async def get_character(character_name: str):
    """Get a specific character's details."""
    if character_name not in CHARACTERS:
        raise HTTPException(status_code=404, detail="Character not found")
    
    char = CHARACTERS[character_name]
    return {
        "name": char.name,
        "base_system_prompt": char.base_system_prompt,
        "personality_traits": {k.value: v for k, v in char.personality_traits.items()},
        "temperature": char.temperature,
    }


@app.post("/api/conversations/run")
async def run_conversation(request: ConversationRequest):
    """Start a new conversation."""
    # Validate characters exist
    for char_name in request.character_names:
        if char_name not in CHARACTERS:
            raise HTTPException(
                status_code=400,
                detail=f"Character '{char_name}' not found",
            )
    
    # Validate turn order
    for speaker in request.turn_order:
        if speaker not in request.character_names:
            raise HTTPException(
                status_code=400,
                detail=f"Speaker '{speaker}' not in character list",
            )
    
    # Get character objects and apply adjustments
    characters = []
    for char_name in request.character_names:
        char = CHARACTERS[char_name]
        char = apply_personality_adjustments(char, request.personality_adjustments)
        characters.append(char)
    
    try:
        # Run conversation
        conversation_log = CONVERSATION_MANAGER.run_turns(
            scenario=request.scenario,
            characters=characters,
            turn_order=request.turn_order,
            num_turns=request.num_turns,
        )
        
        # Store conversation
        conversation_id = f"conv_{len(CONVERSATIONS)}"
        CONVERSATIONS[conversation_id] = conversation_log
        
        return {
            "conversation_id": conversation_id,
            "scenario": conversation_log.scenario,
            "messages": [m.to_dict() for m in conversation_log.messages],
            "created_at": conversation_log.created_at,
        }
    
    except Exception as e:
        # User-friendly error for Gemini timeouts
        if "timed out" in str(e) or "Google Gemini API timed out" in str(e):
            raise HTTPException(
                status_code=504,
                detail="The AI took too long to respond. Please try again with a shorter prompt, fewer turns, or fewer characters."
            )
        raise HTTPException(
            status_code=500,
            detail=f"Conversation generation failed: {str(e)}",
        )


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Retrieve a conversation."""
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    log = CONVERSATIONS[conversation_id]
    return log.to_dict()


@app.post("/api/chat/{character_name}")
async def chat_with_character(
    character_name: str,
    conversation_id: str,
    message: ChatMessage = Body(...),
):
    """Chat with a character about a specific scenario."""
    # Validate character exists
    if character_name not in CHARACTERS:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Validate conversation exists
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        conversation_log = CONVERSATIONS[conversation_id]
        
        # Add user message
        CONVERSATION_MANAGER.add_user_message(
            conversation_log=conversation_log,
            user_name=message.character_name,
            message_text=message.content,
        )
        
        # Get character response
        character = CHARACTERS[character_name]
        response = CONVERSATION_MANAGER.generate_character_response_in_context(
            character=character,
            conversation_log=conversation_log,
        )
        
        # Add character response to log
        CONVERSATION_MANAGER.add_user_message(
            conversation_log=conversation_log,
            user_name=character_name,
            message_text=response,
        )
        
        return {
            "character_name": character_name,
            "response": response,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat generation failed: {str(e)}",
        )


@app.post("/api/personalities/save")
async def save_personality_adjustments(
    user_id: str,
    adjustments: List[PersonalityAdjustment],
):
    """Save personality adjustments (for future use with database)."""
    # This endpoint is a placeholder for Firebase integration
    # For now, adjustments are passed per request to /api/conversations/run
    return {
        "message": "Personality adjustments received",
        "user_id": user_id,
        "adjustments_count": len(adjustments),
        "note": "Firebase persistence not yet implemented",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# Error Handlers
# ============================================================================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", 8000)),
        reload=os.getenv("DEBUG", "true").lower() == "true",
    )
