"""Character model for entertainment app."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum


class PersonalityTrait(str, Enum):
    """Personality trait dimensions (0-100 scale)."""
    AGGRESSION = "aggression"
    KINDNESS = "kindness"
    SARCASM = "sarcasm"
    INTELLIGENCE = "intelligence"
    HUMOR = "humor"


@dataclass
class Character:
    """
    Represents an AI character with personality traits and system prompt.
    
    Attributes:
        name: Character full name
        title: Character job title
        gender: Character gender
        birthdate: Character birthdate (YYYY-MM-DD format)
        age: Character age (int or "50+" string)
        backstory: Character's background and personality story
        personality: Short personality description
        base_system_prompt: Core personality and behavior description
        personality_traits: Dict of trait values (0-100 scale)
        model_override: Optional specific LLM model for this character
        temperature: LLM temperature (0.0-1.0) for response generation
    """
    
    name: str
    base_system_prompt: str
    personality_traits: Dict[PersonalityTrait, int] = field(default_factory=dict)
    title: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    age: Optional[Any] = None
    backstory: Optional[str] = None
    personality: Optional[str] = None
    model_override: Optional[str] = None
    temperature: float = 0.9
    voice: Optional[str] = None
    
    def __post_init__(self):
        """Validate personality traits are in valid range."""
        for trait, value in self.personality_traits.items():
            if not 0 <= value <= 100:
                raise ValueError(f"Trait {trait} must be between 0 and 100, got {value}")
    
    def get_adjusted_prompt(self) -> str:
        """
        Generate system prompt adjusted by personality traits.
        
        Applies trait modifiers to the base prompt. For example:
        - High aggression: Add emphasis on being blunt, confrontational
        - High kindness: Add emphasis on being supportive, gentle
        - High sarcasm: Add emphasis on dry humor, irony
        
        Returns:
            Final system prompt with adjustments applied
        """
        prompt = self.base_system_prompt
        
        # Build modifiers based on traits
        modifiers = []
        
        # Aggression modifier
        if self.personality_traits.get(PersonalityTrait.AGGRESSION, 50) > 70:
            modifiers.append(
                "Be aggressive and confrontational. Don't hold back your opinions. "
                "Challenge others directly and without filter."
            )
        elif self.personality_traits.get(PersonalityTrait.AGGRESSION, 50) < 30:
            modifiers.append(
                "Be very gentle and non-confrontational. Avoid any harsh language. "
                "Frame everything diplomatically."
            )
        
        # Kindness modifier
        if self.personality_traits.get(PersonalityTrait.KINDNESS, 50) > 70:
            modifiers.append(
                "Prioritize others' feelings. Be supportive and encouraging. "
                "Look for the good in everyone."
            )
        elif self.personality_traits.get(PersonalityTrait.KINDNESS, 50) < 30:
            modifiers.append(
                "Be indifferent to others' feelings. Prioritize self-interest. "
                "Point out flaws without empathy."
            )
        
        # Sarcasm modifier
        if self.personality_traits.get(PersonalityTrait.SARCASM, 50) > 70:
            modifiers.append(
                "Use heavy sarcasm, dry humor, and irony. Make witty observations. "
                "Never be serious for too long."
            )
        elif self.personality_traits.get(PersonalityTrait.SARCASM, 50) < 30:
            modifiers.append(
                "Avoid sarcasm entirely. Be literal and straightforward. "
                "Express yourself clearly without jokes."
            )
        
        # Intelligence modifier
        if self.personality_traits.get(PersonalityTrait.INTELLIGENCE, 50) > 75:
            modifiers.append(
                "Use sophisticated vocabulary and complex reasoning. "
                "Provide in-depth analysis and technical insights."
            )
        elif self.personality_traits.get(PersonalityTrait.INTELLIGENCE, 50) < 30:
            modifiers.append(
                "Use simple, everyday language. Focus on surface-level observations. "
                "Avoid complex technical details."
            )
        
        # Humor modifier
        if self.personality_traits.get(PersonalityTrait.HUMOR, 50) > 70:
            modifiers.append(
                "Be funny and entertaining. Look for humorous angles on everything. "
                "Make people laugh."
            )
        elif self.personality_traits.get(PersonalityTrait.HUMOR, 50) < 30:
            modifiers.append(
                "Be serious. Avoid jokes and humor. Stay focused on the topic."
            )
        
        # Combine base prompt with modifiers
        if modifiers:
            prompt += "\n\nPersonality Adjustments:\n" + "\n".join(modifiers)
        
        return prompt
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "title": self.title,
            "gender": self.gender,
            "birthdate": self.birthdate,
            "age": self.age,
            "backstory": self.backstory,
            "personality": self.personality,
            "base_system_prompt": self.base_system_prompt,
            "personality_traits": {k.value: v for k, v in self.personality_traits.items()},
            "model_override": self.model_override,
            "temperature": self.temperature,
            "voice": self.voice,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        """Create character from dictionary."""
        traits = {}
        if "personality_traits" in data:
            for key, value in data["personality_traits"].items():
                try:
                    traits[PersonalityTrait(key)] = value
                except ValueError:
                    # Handle old string keys
                    pass
        
        return cls(
            name=data["name"],
            base_system_prompt=data["base_system_prompt"],
            personality_traits=traits,
            title=data.get("title"),
            gender=data.get("gender"),
            birthdate=data.get("birthdate"),
            age=data.get("age"),
            backstory=data.get("backstory"),
            personality=data.get("personality"),
            model_override=data.get("model_override"),
            temperature=data.get("temperature", 0.9),
            voice=data.get("voice"),
        )
