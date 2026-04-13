# 🚀 Setup & Launch Guide

This guide walks you through setting up and launching the Entertainment App with Streamlit and FastAPI.

## 5-Minute Setup

### Step 1: Get an LLM API Key (Choose One)

**Option A: Google Gemini** (Recommended ⭐)
- Free (with API key)
- Fastest responses (2-4 seconds)
- Excellent quality
- Steps:
  1. Go to https://ai.google.dev/
  2. Click "Get API Key"
  3. Create new API key for Entertainment App
  4. Copy the key (keep it safe!)

**Option B: OpenAI**
- Paid (but cheap to test)
- Very fast (1-2 seconds)
- Excellent quality
- Get key: https://platform.openai.com/

**Option C: Anthropic**
- Paid
- Good quality (5-10 seconds)
- Get key: https://console.anthropic.com/

**Option D: Ollama** (Free but slower)
- Completely free (runs locally)
- Slower (5-15 seconds without GPU)
- No API key needed
- Install: https://ollama.ai/

### Step 2: Create Configuration File

Create a file named `.env` in the `backend` folder with your LLM details:

**For Google Gemini:**
```env
LLM_PROVIDER=google
GOOGLE_API_KEY=your_actual_api_key_here
GOOGLE_MODEL=gemini-pro
```

**For OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

**For Anthropic:**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-2
```

**For Ollama (no API key needed):**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Step 3: Install Python Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r backend/requirements.txt
```

This installs:
- FastAPI (backend framework)
- Streamlit (frontend)
- LLM provider libraries
- Other utilities

### Step 4: Run the Application

**Option A - Easy Launch (Windows)**

Double-click `run_app.bat` - this starts everything automatically.

**Option B - Manual Launch**

Terminal 1 (Backend):
```bash
cd backend
python main.py
```

Terminal 2 (Frontend):
```bash
streamlit run streamlit_app.py
```

### Step 5: Use the App

- **Backend API**: http://localhost:8000/docs (see all endpoints)
- **Frontend App**: http://localhost:8501 (the Streamlit interface)

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"

**Fix**: Install dependencies
```bash
pip install -r backend/requirements.txt
```

### "Connection refused" / Cannot access http://localhost:8000

**Fix**: Backend isn't running
1. Open new terminal
2. Run: `cd backend && python main.py`
3. Wait for "Application startup complete" message

### "Invalid API key" error

**Fix**: 
1. Check your `.env` file exists in `backend/` folder
2. Verify API key is correct (no extra spaces)
3. Check API key has proper permissions in provider dashboard

### "backend/.env" not found

**Fix**:
1. Copy `.env.example` to `.env`:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Edit `backend/.env` and add your API key

### Streamlit says "No internet connection"

**Fix**: If using Google/Anthropic/OpenAI, you DO need internet. If using Ollama:
1. Make sure Ollama is running
2. Check `LLM_PROVIDER=ollama` in `.env`
3. Verify `OLLAMA_BASE_URL=http://localhost:11434`

## What to Try First

### Quick Test (Using Mock LLM)
```bash
cd backend
python test_core.py
```

This tests the conversation engine without needing any API keys. All tests should pass. ✓

### API Documentation
Open http://localhost:8000/docs while backend is running to see:
- All available endpoints
- Request/response schemas
- Try endpoints directly in browser

### Example Scenarios to Test

1. **"Team Decision"**
   - Characters: Strict Boss, Lazy Lead
   - Expected: Conflict between work-focused and avoidant personalities

2. **"New Feature Design"**
   - Characters: Overachieving Teammate, Gen Z Intern
   - Expected: Different approaches to modern development

3. **"Secret Lunch Spot"**
   - Characters: Secret Admirer, Sarcastic Janitor
   - Expected: Funny observations about coworkers

4. **"Project Due Tomorrow"**
   - Characters: Any 3-4 different characters
   - Expected: Realistic team dynamics

## Architecture Overview

```
┌─────────────────────────────────────────┐
│     Streamlit Frontend                  │
│  (streamlit_app.py - 880 lines)        │
│                                         │
│  • Scenario Builder                     │
│  • Live Simulation View                 │
│  • Character Chat                       │
│  • Personality Editor                   │
│  • Replay & What-If                     │
└────────────┬────────────────────────────┘
             │ HTTP Requests
             │ (http://localhost:8000)
             ▼
┌─────────────────────────────────────────┐
│     FastAPI Backend                     │
│  (backend/main.py - 500+ lines)        │
│                                         │
│  API Endpoints:                         │
│  • /api/characters                      │
│  • /api/conversations/run               │
│  • /api/chat/{character}                │
└────────────┬────────────────────────────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
┌──────┐┌───────┐┌─────────┐
│Char. ││Conv.  ││LLM      │
│Model ││Engine ││Provider │
└──────┘└───────┘└─────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌──────────┐    ┌─────────────┐
│JSON File │    │LLM API      │
│(config)  │    │(Google/etc) │
└──────────┘    └─────────────┘
```

## File Layout

```
project/
├── streamlit_app.py        ← Frontend (start here!)
├── run_app.bat             ← Easy launcher (Windows)
├── SETUP.md                ← This file
├── README.md               ← Project overview
│
└── backend/
    ├── main.py             ← FastAPI app (start backend here)
    ├── requirements.txt    ← Python dependencies
    ├── .env.example        ← Copy to .env and add API key
    ├── .env                ← YOUR API KEYS (don't share!)
    ├── test_core.py        ← Test the conversation engine
    │
    ├── models/
    │   └── character.py    ← Character class with traits
    ├── engines/
    │   └── conversation.py ← Conversation logic
    ├── providers/
    │   └── llm_provider.py ← LLM integration (OpenAI, Google, etc)
    ├── config/
    │   └── characters.json ← 6 pre-built characters
    └── db/
        └── firebase.py     ← Database (not yet implemented)
```

## Next Steps

1. ✅ Get API key
2. ✅ Create `.env` file
3. ✅ Install dependencies
4. ✅ Run the app
5. 🎮 Test with example scenarios
6. 📝 Create your own scenarios
7. 🎛️ Adjust character personalities
8. 🔄 Use what-if to explore variations

## Tips & Tricks

- **Slow responses?** Switch from Ollama to Google Gemini
- **Want to test code?** Run `python backend/test_core.py`
- **Need to restart?** Kill terminal (Ctrl+C) and rerun
- **Hot reload?** Streamlit auto-reloads on code changes
- **API testing?** Visit http://localhost:8000/docs

## Getting Help

1. Check **Troubleshooting** section above
2. View **STREAMLIT_FRONTEND.md** for frontend features
3. View **backend/README.md** for API details
4. Check **backend/main.py** for endpoint implementations
5. Review **backend/test_core.py** to understand how the engine works

---

**Ready?** Let's go!

```bash
streamlit run streamlit_app.py
```

Enjoy the app! 🎭
