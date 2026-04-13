"""
Test script for core conversation engine.
Tests character loading, prompt adjustment, and conversation loop (with mock LLM).
"""

import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from models.character import Character, PersonalityTrait
from engines.conversation import ConversationManager, ConversationLog
from providers.llm_provider import ProviderFactory, LLMProvider
from typing import List, Dict, Any


class MockLLMProvider(LLMProvider):
    """Mock LLM for testing without API keys."""
    
    def __init__(self):
        self.call_count = 0
        # Pre-scripted responses for testing
        self.responses = {
            "Strict Boss": [
                "This deadline is unacceptable. Where's the report?",
                "I need results, not excuses. What's the status?",
                "This is a disaster. Someone needs to be held accountable.",
            ],
            "Lazy Lead": [
                "Honestly, this situation is emotionally draining me.",
                "I've been under so much pressure lately...",
                "Nobody appreciates my efforts anymore.",
            ],
            "Overachieving Teammate": [
                "I've already completed my portion. It's well-organized and documented.",
                "We should implement a more structured approach to prevent this.",
                "I can help coordinate the remaining work if needed.",
            ],
            "Gen Z Intern": [
                "We coulda automated this in like 2 hours, just saying.",
                "This deadline was always unrealistic ngl.",
                "I can probably fix this quickly, but it's not ideal.",
            ],
        }
        self.response_idx = 0
    
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = None,
    ) -> str:
        """Return mock response."""
        # Extract character name from system prompt
        system_msg = messages[0].get("content", "")
        
        # Find which character this is
        character_name = None
        for name in self.responses.keys():
            if name.lower() in system_msg.lower():
                character_name = name
                break
        
        if character_name and character_name in self.responses:
            responses = self.responses[character_name]
            response = responses[self.response_idx % len(responses)]
            self.response_idx += 1
            return response
        
        return f"Mock response #{self.call_count}"


def load_characters() -> Dict[str, Character]:
    """Load character definitions from config."""
    config_path = os.path.join(os.path.dirname(__file__), "config", "characters.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    
    characters = {}
    for char_data in config["characters"]:
        char = Character.from_dict(char_data)
        characters[char.name] = char
    
    return characters


def test_character_loading():
    """Test 1: Character loading from config."""
    print("\n" + "=" * 70)
    print("TEST 1: Loading Characters from Config")
    print("=" * 70)
    
    chars = load_characters()
    print(f"✓ Loaded {len(chars)} characters:")
    for name, char in chars.items():
        print(f"  - {name} (temp={char.temperature})")
    
    return chars


def test_personality_adjustment(character: Character):
    """Test 2: Personality trait adjustments."""
    print("\n" + "=" * 70)
    print("TEST 2: Personality Trait Adjustment")
    print("=" * 70)
    
    print(f"\nOriginal {character.name}:")
    print(f"  Traits: {character.personality_traits}")
    
    # Adjust personality
    adjusted_traits = character.personality_traits.copy()
    adjusted_traits[PersonalityTrait.AGGRESSION] = 90
    adjusted_traits[PersonalityTrait.SARCASM] = 85
    
    adjusted_char = Character(
        name=character.name,
        base_system_prompt=character.base_system_prompt,
        personality_traits=adjusted_traits,
        temperature=character.temperature,
    )
    
    print(f"\nAdjusted {character.name}:")
    print(f"  Traits: {adjusted_char.personality_traits}")
    
    print(f"\nBase Prompt (first 100 chars):\n{character.base_system_prompt[:100]}...")
    print(f"\nAdjusted Prompt (shows personality modifications):")
    adjusted_prompt = adjusted_char.get_adjusted_prompt()
    # Show just the adjustments part
    if "Personality Adjustments:" in adjusted_prompt:
        adjustments_part = adjusted_prompt.split("Personality Adjustments:")[1]
        print(adjustments_part[:300])
    
    return adjusted_char


def test_conversation_engine():
    """Test 3: Full conversation loop with mock LLM."""
    print("\n" + "=" * 70)
    print("TEST 3: Conversation Engine with Mock LLM")
    print("=" * 70)
    
    # Load characters
    chars = load_characters()
    
    # Create manager with mock provider
    mock_provider = MockLLMProvider()
    manager = ConversationManager(llm_provider=mock_provider)
    
    # Define conversation
    scenario = "Project deadline is tomorrow but work is incomplete."
    character_list = ["Strict Boss", "Lazy Lead", "Gen Z Intern"]
    turn_order = ["Strict Boss", "Lazy Lead", "Gen Z Intern"]
    
    character_objects = [chars[name] for name in character_list]
    
    print(f"\nScenario: {scenario}")
    print(f"Characters: {character_list}")
    print(f"Turn Order: {turn_order}")
    print(f"Turns: 6\n")
    
    # Run conversation
    log = manager.run_turns(
        scenario=scenario,
        characters=character_objects,
        turn_order=turn_order,
        num_turns=6,
    )
    
    print("\n--- Full Conversation Log ---")
    print(log.get_conversation_text())
    
    print(f"✓ Conversation completed with {len(log.messages)} messages")
    
    return log


def test_conversation_serialization(log: ConversationLog):
    """Test 4: Conversation serialization to JSON."""
    print("\n" + "=" * 70)
    print("TEST 4: Conversation Serialization")
    print("=" * 70)
    
    log_dict = log.to_dict()
    json_str = json.dumps(log_dict, indent=2)
    
    print(f"✓ Serialized conversation to JSON ({len(json_str)} bytes)")
    print(f"  - Scenario: {log_dict['scenario']}")
    print(f"  - Characters: {len(log_dict['characters'])}")
    print(f"  - Messages: {len(log_dict['messages'])}")
    print(f"  - Created: {log_dict['created_at']}")
    
    # Show sample of JSON
    print("\nSample JSON (first 400 chars):")
    print(json_str[:400] + "...")
    
    return log_dict


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("ENTERTAINMENT APP - CORE ENGINE TESTS")
    print("=" * 70)
    
    try:
        # Test 1: Load characters
        characters = test_character_loading()
        
        # Test 2: Personality adjustment on Strict Boss
        test_char = characters["Strict Boss"]
        test_personality_adjustment(test_char)
        
        # Test 3: Full conversation
        conversation_log = test_conversation_engine()
        
        # Test 4: Serialization
        test_conversation_serialization(conversation_log)
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        print("\nBackend core is ready!")
        print("Next steps:")
        print("  1. Set up LLM API keys in .env file")
        print("  2. Run: python main.py")
        print("  3. FastAPI docs available at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
