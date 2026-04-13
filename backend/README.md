## Demo Video

[![Watch the demo on YouTube](https://img.youtube.com/vi/2LioVSmjW-A/0.jpg)](https://youtu.be/2LioVSmjW-A)

<!-- Place your backend screenshot at assets/backend_demo.jpg in the project root. To use a different image or filename, change the path above. -->
# Entertainment App Backend

Python FastAPI backend for the LLM-powered entertainment app.

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your LLM credentials
```

### 3. Run Server

```bash
python main.py
```

Server runs on `http://localhost:8000`
API docs: `http://localhost:8000/docs`

## LLM Provider Setup

### OpenAI (Recommended for quality)

1. Get API key: https://platform.openai.com/api-keys
2. Set in `.env`:
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-xxxxxxxxxxxx
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

### Anthropic (Good alternative)

1. Get API key: https://console.anthropic.com
2. Set in `.env`:
   ```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
   ANTHROPIC_MODEL=claude-3-sonnet-20240229
   ```

### Ollama (Local, free, requires setup)

1. Install Ollama: https://ollama.ai
2. Pull model: `ollama pull mistral`
3. Run server: `ollama serve`
4. Set in `.env`:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=mistral
   ```

## Project Structure

```
backend/
├── config/
│   └── characters.json          # Character definitions & base system prompts
├── db/
│   └── firestore_config.py      # Firebase setup (placeholder)
├── engines/
│   └── conversation.py          # ConversationManager class
├── models/
│   ├── __init__.py
│   └── character.py             # Character class with personality traits
├── providers/
│   ├── __init__.py
│   └── llm_provider.py          # LLM abstraction layer (multipart)
├── main.py                      # FastAPI app & API endpoints
├── test_core.py                 # Tests (uses mock LLM)
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

### Characters

**Get all characters**
```
GET /api/characters
```

**Get specific character**
```
GET /api/characters/{name}
```

### Conversations

**Start conversation**
```
POST /api/conversations/run
{
  "scenario": "Project deadline is tomorrow...",
  "character_names": ["Strict Boss", "Lazy Lead"],
  "turn_order": ["Strict Boss", "Lazy Lead", "Strict Boss"],
  "num_turns": 12,
  "personality_adjustments": [
    {
      "character_name": "Strict Boss",
      "traits": {
        "aggression": 90,
        "sarcasm": 85
      }
    }
  ]
}
```

**Get conversation**
```
GET /api/conversations/{conversation_id}
```

### Chat

**Chat with character**
```
POST /api/chat/{character_name}?conversation_id={id}
{
  "character_name": "Strict Boss",
  "content": "What should I do next?"
}
```

## Core Classes

### Character

Represents an AI character with personalities.

```python
from models.character import Character, PersonalityTrait

boss = Character(
    name="Strict Boss",
    base_system_prompt="You are a strict boss...",
    personality_traits={
        PersonalityTrait.AGGRESSION: 75,
        PersonalityTrait.KINDNESS: 30,
    }
)

# Get prompt with trait modifiers applied
adjusted_prompt = boss.get_adjusted_prompt()
```

### ConversationManager

Manages multi-character conversations.

```python
from engines.conversation import ConversationManager
from models.character import Character

manager = ConversationManager()

log = manager.run_turns(
    scenario="Project deadline tomorrow",
    characters=[boss, lead, intern],
    turn_order=["Strict Boss", "Lazy Lead", "Gen Z Intern"],
    num_turns=12
)

# Access results
messages = log.messages
full_text = log.get_conversation_text()
```

### LLM Providers

Abstract interface with multiple implementations.

```python
from providers.llm_provider import ProviderFactory

# Create provider (auto-detects from LLM_PROVIDER env var)
provider = ProviderFactory.create()

# Or specify explicitly
provider = ProviderFactory.create(provider_name="openai")

# Generate response
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"}
]

response = provider.create_completion(
    messages=messages,
    temperature=0.7,
    max_tokens=150
)
```

## Testing

### Run Core Engine Tests

```bash
python test_core.py
```

This runs tests with a mock LLM (no API keys needed):
1. ✓ Character loading from config
2. ✓ Personality trait adjustment
3. ✓ Conversation loop
4. ✓ Serialization to JSON

### Test with FastAPI Docs

1. Start server: `python main.py`
2. Open: http://localhost:8000/docs
3. Try endpoints interactively

## Character System

### 6 Pre-built Characters

Each character has:
- Base system prompt (defines archetype)
- Default personality traits (0-100 scale)
- Temperature for LLM sampling
- Can be dynamically adjusted

### Personality Traits

- **Aggression** (0-100) - How confrontational
- **Kindness** (0-100) - Empathy level
- **Sarcasm** (0-100) - Humor style
- **Intelligence** (0-100) - Response depth
- **Humor** (0-100) - Comedy level

### How Traits Work

1. Base system prompt defines character
2. Trait values generate modifiers
3. Final prompt = base + modifiers
4. Example: High aggression + sarcasm = blunt, witty

```python
# Original trait
{"aggression": 75, "sarcasm": 40}

# Adjust for higher aggression & sarcasm
{"aggression": 90, "sarcasm": 85}

# get_adjusted_prompt() returns:
# "You are a strict boss...
#  Personality Adjustments:
#  Be aggressive and confrontational. Don't hold back...
#  Use heavy sarcasm, dry humor, and irony..."
```

## Conversation Flow

1. **Load characters** from config/characters.json
2. **For each turn:**
   - Select speaker from turn_order list
   - Build context from last 10 messages
   - Generate final system prompt (base + trait adjustments)
   - Call LLM with context
   - Add response to log
3. **Return full conversation log** with all messages

## Performance Notes

- **LLM calls**: ~2-4 seconds per response (depends on model)
- **12-turn conversation**: ~30-45 seconds (openai/anthropic) 
- **Context window**: Keeps last 10 messages for performance
- **Parallel requests**: Not implemented yet (could speed up)

## Firebase Integration (Optional)

Currently a placeholder for future enhancement:

```python
from db.firestore_config import init_firestore

# Future: Save conversations to Firestore
# db = init_firestore()
# db.collection('conversations').document(id).set(log.to_dict())
```

## Troubleshooting

### Import errors
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### LLM API errors
- Check API keys in `.env`
- Verify API service status
- Check rate limits
- Ensure API has required permissions

### Conversation generation fails
- Check turn_order characters exist in character_names
- Verify LLM provider is working (test in docs)
- Check LLM API limits

### Port already in use
- Change SERVER_PORT in .env
- Or: `python main.py` then Ctrl+C, wait, try again

## Development

### Add Custom Character

1. Edit `config/characters.json`
2. Add new entry:
   ```json
   {
     "name": "New Character",
     "base_system_prompt": "You are...",
     "personality_traits": {
       "aggression": 50,
       "kindness": 50,
       ...
     }
   }
   ```
3. Restart server

### Add New LLM Provider

1. Create class in `providers/llm_provider.py`
2. Inherit from `LLMProvider`
3. Implement `create_completion()` method
4. Register in `ProviderFactory._providers`

```python
class MyProvider(LLMProvider):
    def create_completion(self, messages, temperature=0.7, max_tokens=None):
        # Your implementation
        return response
```

## Next Steps

- Add Firebase persistence
- Implement real-time WebSocket streaming
- Add character memory across scenarios
- Create admin interface for character management
- Add conversation analytics/metrics

---

For full project documentation, see [../README.md](../README.md)
