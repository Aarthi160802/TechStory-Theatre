# TechStory Theatre

## Demo

[![TechStory Theatre Demo](<img width="1366" height="768" alt="Capture" src="https://github.com/user-attachments/assets/51c29a81-6c81-473e-89d8-5ce36cf6623b" />
)](https://youtu.be/2LioVSmjW-A)

## Overview
TechStory Theatre is an interactive, LLM-powered entertainment app where AI-driven characters with unique personalities interact in realistic workplace scenarios. Users can watch, configure, and even participate in these conversations, making it a fun and educational tool for understanding team dynamics, communication, and workplace culture.

## Features
- **Streamlit Frontend:** Simple, modern UI for scenario selection, cast configuration, and live simulation.
- **FastAPI Backend:** Robust API for managing characters, conversations, and LLM integration.
- **Character Personalities:** Each character has a detailed backstory, personality traits, and unique conversational style inspired by workplaces.
- **Scenario Suggestions:** Predefined scene ideas for team drama, project crises, and more.
- **User Participation:** Users can join the conversation as any character.
- **Personality Tuning:** Adjust character traits and apply them live.
- **Conversation Saving:** Save and review past conversations.
- **Persistence:** Conversations are saved locally for replay and analysis.

## Code Structure
```
backend/
   config/characters.json      # All character and company data
   engines/                    # Conversation logic and LLM orchestration
   main.py                     # FastAPI app entry point
   models/character.py         # Character dataclass and serialization
   providers/llm_provider.py   # LLM provider abstraction (Google Gemini, etc)
frontend/
   streamlit_app.py            # Main Streamlit UI
conversations/                # Saved conversation logs
.env, .env.example            # Environment variables (API keys, etc)
README.md                     # This documentation
```

## Requirements
- Python 3.9+
- Streamlit
- FastAPI
- requests
- python-dotenv
- Google Generative AI SDK (for Gemini)
- (See requirements.txt for full list)

## Character Information & Importance
Characters are the heart of TechStory Theatre. Each has:
- **Name, Title, Age, Gender**
- **Backstory:** Written in simple, Indian-style for relatability
- **Personality Traits:** Aggression, Kindness, Sarcasm, Intelligence, Humor
- **System Prompt:** Guides the LLM to speak in the character’s voice

This realism makes conversations engaging and educational, reflecting real workplace interactions.

## Conversation Memory & Time Issues
- **Current:** Each conversation is saved locally, but characters do not remember past scenarios across sessions.
- **Future Enhancements:**
   - Implement long-term memory so characters can recall previous conversations and user interactions.
   - Allow users to remind characters of past scenarios and see how their responses change.
   - Add time-travel or flashback features for richer storytelling.

## User Interaction
- Users can join as any character and send messages.
- Personality traits can be tuned and applied live.
- Saved conversations can be reviewed and replayed.

## How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Set up `.env` with your API keys (see `.env.example`).
3. Start the backend: `uvicorn backend.main:app --reload`
4. Start the frontend: `streamlit run streamlit_app.py`

## Future Enhancements
- Long-term character memory
- More scenario templates
- Multi-user support
- Video/audio integration (see placeholder above)
- Improved UI/UX
- Analytics on conversation quality

## License
This project is for educational/demo purposes. Please do not use real company or personal data.
# 🎭 Entertainment App - Full Implementation

An LLM-powered interactive entertainment application where users create scenarios and watch AI characters with different personalities interact with each other. Users can customize character personalities, intervene in conversations, and chat with individual characters about the scenario.

## 🎯 Project Overview

### Core Features

1. **Scenario Builder** - Input a scenario and select characters to participate
2. **Live Simulation** - Watch characters interact with user-controlled turn-taking
3. **Character Chat** - Talk directly to characters about the scenario
4. **Personality Editor** - Adjust character traits with sliders (aggression, kindness, sarcasm, intelligence, humor)
5. **Replay/What-If** - Re-run scenarios with modified parameters

### Characters (6 Pre-built)

- 👔 **Strict Boss** - Disciplined, impatient, results-focused
- 🎭 **Lazy Lead** - Dramatic, avoids work, emotional
- 🏆 **Overachieving Teammate** - Perfectionist, hardworking, stressed
- 🤓 **Gen Z Intern** - Intelligent, witty, casual
- 💖 **Secret Admirer** - Polite, kind, subtle support
- 🧹 **Sarcastic Janitor** - Observant, witty, detached

## 🏗️ Project Structure

```
.
├── backend/                          # Python FastAPI backend
│   ├── config/
│   │   └── characters.json          # Character definitions & base prompts
│   ├── db/                          # Database utilities (Firebase placeholder)
│   ├── engines/
│   │   └── conversation.py          # Conversation engine & turn-taking logic
│   ├── models/
│   │   └── character.py             # Character class with personality traits
│   ├── providers/
│   │   └── llm_provider.py          # LLM abstraction (OpenAI, Anthropic, Ollama)
│   ├── main.py                      # FastAPI app & endpoints
│   ├── test_core.py                 # Core engine tests (mock LLM)
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Environment variables template
│
├── frontend/                         # React + TypeScript frontend
│   ├── src/
│   │   ├── screens/
│   │   │   ├── ScenarioBuilder.tsx   # Screen 1: Create scenario
│   │   │   ├── SimulationView.tsx    # Screen 2: Watch interaction
│   │   │   ├── ChatWithCharacter.tsx # Screen 3: Chat with character
│   │   │   ├── PersonalityEditor.tsx # Screen 4: Adjust traits
│   │   │   ├── ReplayWhatIf.tsx      # Screen 5: Replay scenarios
│   │   │   └── screens.css           # Screen styles
│   │   ├── components/
│   │   │   ├── index.ts             # Reusable UI components
│   │   │   └── components.css       # Component styles
│   │   ├── services/
│   │   │   └── api.ts              # API service layer
│   │   ├── store/
│   │   │   └── appStore.ts         # Zustand state management
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript type definitions
│   │   ├── App.tsx                 # Main app orchestrator
│   │   ├── App.css                 # Global styles
│   │   ├── main.tsx                # Entry point
│   │   └── index.css               # Base styles
│   ├── public/                      # Static assets
│   ├── package.json                # Node dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tsconfig.json               # TypeScript configuration
│   └── README.md                    # Frontend documentation
│
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- LLM API key (Google Gemini, OpenAI, Anthropic, or local Ollama)

**Option A: Streamlit** (Recommended - Simpler)
- No Node.js needed
- Single Python file frontend
- Fastest setup

**Option B: React** (Advanced - Full features)
- Node.js 18+
- TypeScript frontend
- More customization

### Backend Setup

1. **Create Python virtual environment**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or: source .venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your LLM API keys
   ```

4. **Test core engine** (optional, uses mock LLM)
   ```bash
   python test_core.py
   ```

5. **Run FastAPI server**
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000`
   API docs: `http://localhost:8000/docs`

### Frontend Setup - Option A: Streamlit (Recommended ⭐)

1. **Run Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```
   Frontend opens at `http://localhost:8501`

📖 **Full guide**: See [STREAMLIT_FRONTEND.md](STREAMLIT_FRONTEND.md)

### Frontend Setup - Option B: React

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`

3. **Build for production**
   ```bash
   npm run build
   ```

📖 **Full guide**: See [frontend/README.md](frontend/README.md)

## 🔧 Configuration

### Backend (.env)

```env
# LLM Settings
LLM_PROVIDER=openai  # openai, anthropic, ollama
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OLLAMA_BASE_URL=http://localhost:11434

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=true

# Firebase (optional for persistence)
FIREBASE_CREDENTIALS_PATH=./firebase-key.json
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 📖 API Endpoints

### Characters

- `GET /api/characters` - Get all characters
- `GET /api/characters/{name}` - Get single character details

### Conversations

- `POST /api/conversations/run` - Start new conversation
  ```json
  {
    "scenario": "Project deadline tomorrow...",
    "character_names": ["Strict Boss", "Lazy Lead"],
    "turn_order": ["Strict Boss", "Lazy Lead", "Strict Boss"],
    "num_turns": 12,
    "personality_adjustments": [
      {
        "character_name": "Strict Boss",
        "traits": { "aggression": 90, "sarcasm": 85 }
      }
    ]
  }
  ```
- `GET /api/conversations/{id}` - Fetch conversation log

### Chat

- `POST /api/chat/{character_name}` - Chat with character about scenario

## 🎮 Usage

### Basic Flow

1. **Open app** → `http://localhost:5173`
2. **Create scenario** → Enter description, select characters
3. **Set turn order** → Click characters to build speaking order
4. **Watch simulation** → Characters interact with you controlling turns
5. **Optional: Chat** → Click a character to chat directly
6. **Optional: Adjust traits** → Edit personality sliders and replay

### Example Scenarios

- "Project deadline is tomorrow but work is incomplete"
- "Team meeting to discuss budget cuts"
- "New technology needs to be adopted immediately"
- "Someone accidentally shipped production to production"

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **LLM**: OpenAI, Anthropic, Ollama (abstracted)
- **Database**: Firebase Firestore (optional for persistence)
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18 with TypeScript
- **Build**: Vite
- **State**: Zustand
- **HTTP**: Axios
- **Styling**: CSS3

## 📊 Character System

### Personality Traits

Each character has 5 adjustable traits (0-100 scale):

- **Aggression** - How confrontational/blunt (0=gentle, 100=aggressive)
- **Kindness** - Empathy and support (0=selfish, 100=very kind)
- **Sarcasm** - Humor style (0=literal, 100=very sarcastic)
- **Intelligence** - Depth of responses (0=simple, 100=sophisticated)
- **Humor** - Comedy level (0=serious, 100=hilarious)

### Prompt Engineering

Base system prompts are dynamically adjusted based on trait values:

```python
character = Character(
    name="Strict Boss",
    base_system_prompt="You are a strict boss...",
    personality_traits={
        PersonalityTrait.AGGRESSION: 75,
        PersonalityTrait.KINDNESS: 30,
        # ...
    }
)

# get_adjusted_prompt() adds trait-based modifiers
adjusted = character.get_adjusted_prompt()
# Returns base prompt + "Be aggressive and confrontational..." etc.
```

## 🔄 Conversation Flow

1. **User creates scenario** → "Project deadline is tomorrow"
2. **User selects characters** → Boss, Lead, Intern
3. **User sets turn order** → [Boss, Lead, Intern, Boss, Lead, Intern]
4. **Backend processes**:
   - Load character definitions
   - Apply personality adjustments (if any)
   - For each turn:
     - Build context from conversation history
     - Generate system prompt with character personality
     - Call LLM with context
     - Store response in log
5. **Frontend displays** → Live message stream with speaker avatars
6. **User controls** → Click "Next Turn" to generate each response

## 🎨 UI/UX Features

- **Responsive design** - Works on desktop and tablet
- **Real-time streaming** - Messages appear as they're generated (future enhancement)
- **Character cards** - Visual selection with trait indicators
- **Personality sliders** - Real-time trait adjustment with preview
- **Chat interface** - Natural conversation with selected character
- **Conversation history** - Keep recent scenarios for replay
- **Speed control** - Adjust playback speed (future enhancement)

## 🚧 Future Enhancements

### Phase 2 Roadmap

1. **Real-time streaming** - WebSocket support for live message streaming
2. **Firebase persistence** - Full cloud storage of conversations
3. **Interrupt mode** - Characters cut each other off mid-response
4. **Conflict meter** - Visual drama level indicator
5. **Episode titles** - Auto-generated titles using LLM
6. **Custom characters** - Create entirely new characters
7. **Memory system** - Characters remember past scenarios
8. **Export** - Download conversations as PDF/JSON
9. **Async turns** - Multiple characters speaking simultaneously
10. **Audio** - Voice synthesis for character responses

## 🧪 Testing

### Backend Testing

```bash
# Test core engine with mock LLM
cd backend
python test_core.py

# Test API endpoints
# (Use FastAPI docs at http://localhost:8000/docs)
```

### Frontend Testing

```bash
cd frontend
npm run lint    # Check for linting issues
npm run build   # Build and check for errors
```

## 📝 Environment Setup Guide

### For OpenAI

1. Get API key from https://platform.openai.com/api-keys
2. Set in backend/.env:
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-xxxx
   ```

### For Anthropic

1. Get API key from https://console.anthropic.com
2. Set in backend/.env:
   ```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-xxxx
   ```

### For Local Ollama

1. Install Ollama: https://ollama.ai
2. Run: `ollama pull mistral`
3. Set in backend/.env:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   ```

## 🎓 Key Concepts

### Character Prompt Engineering

The system prompt is the key to character behavior. It combines:

1. **Base prompt** - Character archetype and goals
2. **Trait modifiers** - Dynamic adjustments based on sliders
3. **Context** - Recent conversation history
4. **Instructions** - Output format and length

### Turn-Taking Logic

Currently **user-directed**:
- User sees next speaker recommendation
- User clicks "Next Turn" to generate response
- User can manually adjust turn order

Future: **Smart logic** could use LLM to determine natural speaker.

### Personality Adjustment System

Traits are multiplicative:
- **Base traits** define character defaults
- **Slider adjustments** modify base values
- **Final prompt** includes both base + modifications
- **Example**: Strict Boss with high sarcasm = "aggressive AND witty"

## 🐛 Troubleshooting

### Backend won't start
- Check Python version (3.10+)
- Verify .env file exists with API keys
- Check if port 8000 is available

### Frontend won't load
- Ensure backend is running (check http://localhost:8000/docs)
- Clear browser cache (Ctrl+Shift+Delete)
- Check console for CORS errors

### LLM API errors
- Verify API keys are correct
- Check if API service is accessible
- For OpenAI: verify account has credits
- For Anthropic: verify API key permissions

### Conversations not generating
- Check backend logs for API errors
- Verify turn_order characters exist in character_names
- Check LLM request limits

## 📄 License

This project is provided as-is for educational and entertainment purposes.

## 🤝 Contributing

Feel free to fork, modify, and extend this project!

### Extension Ideas
- Add more character archetypes
- Implement different conversation styles (debate, storytelling, etc.)
- Add multi-language support
- Create mobile app version
- Add video/audio synthesis
- Implement character relationships

---

**Happy creating! 🎬**
