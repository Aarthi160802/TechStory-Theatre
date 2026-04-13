# Streamlit Frontend - Entertainment App

This is the Streamlit-based frontend for the LLM-powered entertainment app. It's simpler and faster to set up than the React version.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment
Create a `backend/.env` file:
```env
LLM_PROVIDER=google
GOOGLE_API_KEY=your_actual_api_key_here
GOOGLE_MODEL=gemini-pro
```

Or use other providers:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Start Backend Server
```bash
cd backend
python main.py
```
The API will be available at http://localhost:8000

### 4. Run Streamlit App
In a new terminal:
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at http://localhost:8501

## Features

### 1. Scenario Builder
- Create custom scenarios (e.g., "Team meeting about missed deadline")
- Select characters to participate
- Set the order in which characters speak
- Click "Start Conversation" to begin

### 2. Simulation View
- Watch characters interact based on the scenario
- See real-time conversation flow
- Control buttons:
  - **Continue** - Get next character response
  - **Skip Turn** - Move to next character
  - **Reset** - Start over with same scenario
  - **New Scenario** - Go back to builder

### 3. Chat with Character
- Have one-on-one conversations with any character
- Test how personality traits affect responses
- Message history displayed in conversation view
- Characters maintain their personality throughout

### 4. Personality Editor
- Adjust 5 personality traits for any character (0-100 scale):
  - **Aggression**: How confrontational they are
  - **Kindness**: How compassionate they are
  - **Sarcasm**: How sarcastic/witty they are
  - **Intelligence**: How intellectual/complex their responses are
  - **Humor**: How funny/joke-oriented they are
- See real-time changes in next responses
- Adjustments apply to current session only

### 5. Replay & What-If
- Replay previous conversations
- Modify parameters and see different outcomes:
  - Change character personality traits
  - Modify the scenario premise
  - Adjust LLM temperature (creativity level)
- Compare different variations of same scenario

## Supported Characters

1. **Strict Boss** - Demanding, serious, focused on deadlines
2. **Lazy Lead** - Procrastinating, relaxed, problem-minimal
3. **Overachieving Teammate** - Ambitious, hardworking, perfectionist
4. **Gen Z Intern** - Casual, meme-savvy, fresh perspectives
5. **Secret Admirer** - Complimentary, shy, supportive
6. **Sarcastic Janitor** - Witty, observant, darkly humorous

## LLM Providers

### Google Gemini (Recommended)
- **Cost**: Free (with API key)
- **Speed**: 2-4 seconds per response
- **Quality**: Excellent
- **Setup**: Get free API key from https://ai.google.dev/

### OpenAI
- **Cost**: Paid API
- **Speed**: 1-2 seconds per response
- **Quality**: Excellent
- **Setup**: https://platform.openai.com/

### Anthropic
- **Cost**: Paid API
- **Speed**: 5-10 seconds per response
- **Quality**: Excellent
- **Setup**: https://console.anthropic.com/

### Ollama (Local)
- **Cost**: Free (runs locally, no API calls)
- **Speed**: 5-15 seconds per response (CPU-dependent)
- **Quality**: Good (depends on model)
- **Setup**: https://ollama.ai/

## Troubleshooting

### "Connection refused" error
- Ensure backend is running: `python backend/main.py`
- Check port 8000 is available

### "Invalid API key" error
- Verify your `.env` file has correct API key
- Check API key has proper permissions in provider dashboard

### Slow responses
- If using Ollama without GPU, responses will be slow (5-15 sec)
- Switch to Google Gemini for faster responses

### Session state issues
- Clear browser cache or use private/incognito window
- Restart Streamlit app: `streamlit run streamlit_app.py`

## Architecture

```
streamlit_app.py (880 lines)
    ├── Session state initialization
    ├── API functions (load_characters, start_conversation, chat_with_character)
    ├── 5 Screen functions:
    │   ├── scenario_builder()
    │   ├── simulation_view()
    │   ├── chat_with_character_screen()
    │   ├── personality_editor()
    │   └── replay_whatif()
    └── Navigation logic
        └── Calls FastAPI backend at http://localhost:8000
```

## Development

All frontend code is in `streamlit_app.py`. To modify:
1. Edit the file
2. Streamlit will automatically reload on save
3. Check terminal for any errors

## Environment Variables

```env
# Backend server URL
BACKEND_URL=http://localhost:8000

# LLM Provider configuration (in backend/.env)
LLM_PROVIDER=google|openai|anthropic|ollama
[PROVIDER]_API_KEY=...
[PROVIDER]_MODEL=...
```

## Tips for Best Results

1. **Start Simple**: Use "Team Conflict" scenario with Strict Boss + Lazy Lead
2. **Adjust Traits**: Change sarcasm to 100 for funny interactions
3. **Long Scenarios**: Multi-turn conversations reveal more character depth
4. **Replay Often**: Use what-if to explore different personality combinations

---

**Questions?** Check backend/README.md for API details or review streamlit_app.py for code comments.
