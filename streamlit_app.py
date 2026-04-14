"""
TechStory Theatre - AI Character Conversation Engine
Interactive entertainment where you watch and participate in character interactions
"""

import streamlit as st
import requests
import json
import os
import hashlib
import tempfile
from typing import Dict, List, Optional
from datetime import datetime

try:
    import edge_tts
    import asyncio
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="🎭 TechStory Theatre",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

# Company Info
COMPANY_INFO = {
    "name": "TechStory",
    "tagline": "Where Code Meets Story",
    "founded": 2020,
    "mission": "Building the future of interactive entertainment through AI"
}

# Scenario Suggestions
SCENARIO_SUGGESTIONS = {
    "Team Dynamics": [
        "Team meeting about a missed deadline - nobody knows who's responsible",
        "Budget cuts announced - how will different team members react?",
        "New technology needs immediate adoption but nobody knows how to use it",
        "Team member gets an amazing offer from a competing company",
        "Remote work policy is being reversed - back to office!"
    ],
    "Interpersonal Drama": [
        "Someone accidentally spilled coffee on someone's laptop",
        "A secret about the CEO leaks during team lunch",
        "Two team members have conflicting ideas about the next feature",
        "A colleague gets promoted over someone more experienced",
        "Someone's personal drama becomes the office talk"
    ],
    "Project Scenarios": [
        "The product launch is 2 weeks away but features are incomplete",
        "A critical bug was discovered in production",
        "A client demands changes that'll take a month in a week",
        "The team has to choose: ship MVP or wait for perfection",
        "A security vulnerability is found - what now?"
    ],
    "Relationships": [
        "Krish's mom shows up at the office unannounced",
        "Divya's dad wants to invest in the company",
        "Someone finds out about another's secret crush",
        "A team member brings their partner to team lunch",
        "Gossip about someone's personal life spreads in the office"
    ]
}

# ============================================================================
# TTS VOICE CONFIG — each character gets a unique voice + rate/pitch
# ============================================================================

# edge-tts voices:
#   en-US-GuyNeural      = American male (deep)
#   en-US-JennyNeural    = American female
#   en-IN-PrabhatNeural  = Indian male
#   en-IN-NeerjaExpressiveNeural = Indian female (expressive)
# rate/pitch tweaks make same base voice sound distinct per character.

CHARACTER_VOICE_CONFIG = {
    "Krish Sharma":  {"voice": "en-US-GuyNeural",                "rate": "+0%",  "pitch": "+0Hz"},   # US male, deep, CEO authority
    "Divya Singh":   {"voice": "en-US-JennyNeural",              "rate": "+0%",  "pitch": "+0Hz"},   # US female, soft
    "Swetha Patel":  {"voice": "en-IN-PrabhatNeural",            "rate": "+10%", "pitch": "+3Hz"},   # Indian male, energetic/fast
    "Vishnu Kumar":  {"voice": "en-IN-PrabhatNeural",            "rate": "-5%",  "pitch": "-2Hz"},   # Indian male, calm/steady
    "Aadya Saxena":  {"voice": "en-IN-NeerjaExpressiveNeural",   "rate": "+15%", "pitch": "+0Hz"},   # Indian female, young/quick
    "Ramesh Kumar":  {"voice": "en-IN-PrabhatNeural",            "rate": "-20%", "pitch": "-5Hz"},   # Indian male, elder/slow
}

DEFAULT_VOICE_CONFIG = {"voice": "en-IN-PrabhatNeural", "rate": "+0%", "pitch": "+0Hz"}


async def _generate_audio_async(messages: list, combined_path: str) -> str:
    """Generate per-character audio clips and concatenate into one MP3."""
    combined_bytes = bytearray()

    for msg in messages:
        speaker = msg.get("speaker_name", "Unknown")
        content = msg.get("content", "")
        if not content.strip():
            continue

        cfg = CHARACTER_VOICE_CONFIG.get(speaker, DEFAULT_VOICE_CONFIG)
        speech_text = f"{speaker} says: {content}"

        communicate = edge_tts.Communicate(
            speech_text,
            voice=cfg["voice"],
            rate=cfg["rate"],
            pitch=cfg["pitch"],
        )
        # Collect audio bytes from the stream
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                combined_bytes.extend(chunk["data"])

    with open(combined_path, "wb") as f:
        f.write(combined_bytes)

    return combined_path


def _generate_combined_audio(messages: list) -> Optional[str]:
    """Generate a single combined audio file for all messages with character-appropriate voices."""
    if not messages:
        return None

    # Create a cache key from all messages combined
    all_text = "".join(f"{m.get('speaker_name','')}{m.get('content','')}" for m in messages)
    cache_key = hashlib.md5(all_text.encode()).hexdigest()
    cache_dir = os.path.join(tempfile.gettempdir(), "techstory_tts")
    os.makedirs(cache_dir, exist_ok=True)
    combined_path = os.path.join(cache_dir, f"scene_{cache_key}.mp3")

    # Return cached file if it exists
    if os.path.exists(combined_path):
        return combined_path

    try:
        # Run async TTS in a fresh event loop on a background thread
        # to avoid conflicts with Streamlit's own event loop
        import threading
        result = [None, None]  # [success, error]

        def _run():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(_generate_audio_async(messages, combined_path))
                loop.close()
                result[0] = True
            except Exception as ex:
                result[1] = ex

        t = threading.Thread(target=_run)
        t.start()
        t.join(timeout=120)

        if result[1]:
            st.warning(f"Audio generation failed: {result[1]}")
            return None
        return combined_path
    except Exception as e:
        st.warning(f"Audio generation failed: {e}")
        return None


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "characters" not in st.session_state:
    st.session_state.characters = []

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "user_input_enabled" not in st.session_state:
    st.session_state.user_input_enabled = False

if "current_screen" not in st.session_state:
    st.session_state.current_screen = "home"

if "personality_adjustments" not in st.session_state:
    st.session_state.personality_adjustments = {}

# ============================================================================
# API FUNCTIONS
# ============================================================================

def load_characters():
    """Load all characters from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/characters", timeout=5)
        if response.status_code == 200:
            chars = response.json()["characters"]
            return sorted(chars, key=lambda x: x.get("name", ""))
        else:
            st.error(f"Failed to load characters: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend at http://localhost:8000")
        st.info("Make sure to run: python main.py")
    except Exception as e:
        st.error(f"Error loading characters: {str(e)}")
    return []


def start_conversation(scenario: str, character_names: List[str], turn_order: List[str], num_turns: int):
    """Start a new conversation"""
    try:
        payload = {
            "scenario": scenario,
            "character_names": character_names,
            "turn_order": turn_order,
            "num_turns": num_turns,
        }
        response = requests.post(f"{API_BASE_URL}/conversations/run", json=payload, timeout=1200)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                err_data = response.json()
                error_msg = err_data.get("detail") or err_data.get("error") or response.text
            except Exception:
                error_msg = response.text
            # Show user-friendly message for quota errors
            if "quota" in str(error_msg).lower() or "429" in str(error_msg):
                st.error("⏳ API quota limit reached. Please wait a minute and try again, or use a different API key.")
            else:
                st.error(f"API Error {response.status_code}: {error_msg}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timed out - the conversation is taking too long to generate")
        return None
    except Exception as e:
        st.error(f"Failed to start conversation: {str(e)}")
        st.info("Make sure the backend is running on http://localhost:8000")
        return None


def chat_with_character(character_name: str, message: str):
    """Chat with a character"""
    try:
        payload = {
            "character_name": character_name,
            "content": message,
        }
        params = {"conversation_id": st.session_state.current_conversation.get("conversation_id", "")}
        response = requests.post(
            f"{API_BASE_URL}/chat/{character_name}",
            json=payload,
            params=params,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["response"]
    except Exception as e:
        st.error(f"Failed to get response: {str(e)}")
    return None


def save_conversation_locally():
    """Save conversation to local file"""
    if not st.session_state.current_conversation:
        return
    
    conv_data = {
        "timestamp": datetime.now().isoformat(),
        "scenario": st.session_state.current_conversation.get("scenario", ""),
        "messages": st.session_state.current_conversation.get("messages", []),
        "user_messages": st.session_state.conversation_history
    }
    
    # Create conversations directory if it doesn't exist
    os.makedirs("conversations", exist_ok=True)
    
    # Save with date only (no time)
    filename = f"conversations/conversation_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w') as f:
        json.dump(conv_data, f, indent=2)
    return filename


# ============================================================================
# UI COMPONENTS
# ============================================================================

def sidebar_controls():
    """Sidebar with character selection and controls"""
    st.sidebar.title("🎬 TechStory Theatre")
    st.sidebar.caption(COMPANY_INFO["tagline"])
    st.sidebar.divider()
    
    # Character Selection
    st.sidebar.subheader("👥 Cast Selection")
    st.sidebar.caption("Select characters for this scene")
    
    # Arrange characters in the order from characters.json
    order = [
        "Krish Sharma",
        "Swetha Patel",
        "Vishnu Kumar",
        "Aadya Saxena",
        "Divya Singh",
        "Ramesh Kumar"
    ]
    # Emoji and short description for each character
    char_display_map = {
        "Krish Sharma": "👔 Krish Sharma - Ambitious CEO, gets teased about his age",
        "Swetha Patel": "🎭 Swetha Patel - Dramatic, friendly Team Lead, loves gossip",
        "Vishnu Kumar": "💻 Vishnu Kumar - Hardworking, practical Senior Dev",
        "Aadya Saxena": "🦄 Aadya Saxena - Genius Gen Z intern, here for the vibes",
        "Divya Singh": "🌸 Divya Singh - Kind, independent Product Manager",
        "Ramesh Kumar": "🧹 Ramesh Ji - Wise, sarcastic Facilities Manager, company heart"
    }
    # Sort characters by the specified order
    characters = sorted(st.session_state.characters, key=lambda c: order.index(c["name"]) if c["name"] in order else 99)
    selected_chars = []
    for char in characters:
        char_display = char_display_map.get(char["name"], char["name"])
        if st.sidebar.checkbox(
            char_display,
            value=(char["name"] in ["Krish Sharma", "Swetha Patel", "Aadya Saxena"]),
            key=f"select_{char['name']}"
        ):
            selected_chars.append(char["name"])
    
    st.sidebar.divider()
    
    # Turn Order Setup
    st.sidebar.subheader("🎬 Speaking Order")
    
    if "turn_order" not in st.session_state:
        st.session_state.turn_order = []
    
    # Display current order
    if st.session_state.turn_order:
        st.sidebar.caption(f"Order: {' → '.join(st.session_state.turn_order)}")
        if st.sidebar.button("🔄 Reset Order"):
            st.session_state.turn_order = []
            st.rerun()
    else:
        st.sidebar.caption("Select characters above and add them in order")
    
    # Add buttons for selected characters
    cols = st.sidebar.columns(min(3, len(selected_chars)) if selected_chars else 1)
    for idx, char in enumerate(selected_chars):
        with cols[idx % 3]:
            if st.button(f"+ {char.split(' - ')[0]}", key=f"add_{char}", use_container_width=True):
                if char not in st.session_state.turn_order:
                    st.session_state.turn_order.append(char)
                    st.rerun()
    
    st.sidebar.divider()
    
    # Personality Adjustments
    st.sidebar.subheader("🎚️ Personality Tuning")
    st.sidebar.caption("Adjust trait intensities (0-100)")
    
    if selected_chars:
        chosen_char = st.sidebar.selectbox(
            "Choose character to adjust:",
            selected_chars,
            key="personality_char_select"
        )
        if chosen_char:
            char_data = next((c for c in characters if c["name"] == chosen_char), None)
            if char_data:
                traits = char_data.get("personality_traits", {})
                # Temporary state for sliders
                if "_trait_temp" not in st.session_state:
                    st.session_state._trait_temp = {}
                if chosen_char not in st.session_state._trait_temp:
                    st.session_state._trait_temp[chosen_char] = traits.copy()
                for trait in ["aggression", "kindness", "sarcasm", "intelligence", "humor"]:
                    st.session_state._trait_temp[chosen_char][trait] = st.sidebar.slider(
                        f"{trait.title()}",
                        0, 100,
                        st.session_state._trait_temp[chosen_char].get(trait, 50),
                        key=f"slider_{chosen_char}_{trait}"
                    )
                if st.sidebar.button("Apply Personality", key=f"apply_{chosen_char}"):
                    if "personality_adjustments" not in st.session_state:
                        st.session_state.personality_adjustments = {}
                    st.session_state.personality_adjustments[chosen_char] = st.session_state._trait_temp[chosen_char].copy()
                    st.sidebar.success(f"Applied traits to {chosen_char}")
    
    st.sidebar.divider()
    
    # Number of Turns
    st.sidebar.subheader("⏱️ Scene Duration")
    num_turns = st.sidebar.slider("Number of exchanges", 2, 30, 6, key="num_turns_slider")
    
    st.sidebar.divider()
    
    # Company Info
    st.sidebar.subheader("🏢 About TechStory")
    st.sidebar.caption(f"**Founded:** {COMPANY_INFO['founded']}")
    st.sidebar.caption(f"**Mission:** {COMPANY_INFO['mission']}")
    
    return selected_chars, num_turns


def home_screen():
    """Home screen with scenario suggestions"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🎭 TechStory Theatre")
        st.markdown(f"### {COMPANY_INFO['tagline']}")
        st.markdown("Watch AI characters with unique personalities interact in realistic workplace scenarios.")
    
    with col2:
        st.info(f"🏢 **{COMPANY_INFO['name']}**\nSince {COMPANY_INFO['founded']}")
    
    st.divider()
    
    st.subheader("💡 Choose a Scene")
    
    # Scenario Selection
    category = st.selectbox(
        "Scene Category:",
        list(SCENARIO_SUGGESTIONS.keys()),
        key="home_scenario_category"
    )
    
    scenario = st.selectbox(
        "Choose a scenario:",
        SCENARIO_SUGGESTIONS[category],
        key="home_scenario_select"
    )
    
    st.info(f"📖 Scene: {scenario}")
    
    st.divider()
    
    # Get sidebar controls
    selected_chars, num_turns = sidebar_controls()
    
    # Start Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("▶️ Start Scene", type="primary", use_container_width=True):
            if not scenario.strip():
                st.error("Please select a scenario")
            elif not selected_chars:
                st.error("Please select at least one character")
            elif not st.session_state.turn_order:
                st.error("Please set the speaking order")
            else:
                with st.spinner("🎬 Generating scene..."):
                    result = start_conversation(
                        scenario,
                        selected_chars,
                        st.session_state.turn_order,
                        num_turns
                    )
                    if result:
                        st.session_state.current_conversation = result
                        st.session_state.conversation_history = []
                        st.session_state.current_screen = "simulation"
                        st.rerun()


def simulation_screen():
    """Main conversation simulation view"""
    col1, col2 = st.columns([3, 1], gap="large")
    
    with col1:
        st.title("🎬 Live Scene")
        
        if not st.session_state.current_conversation:
            st.warning("No scene loaded")
            if st.button("← Back to Home"):
                st.session_state.current_screen = "home"
                st.rerun()
            return
        
        conv = st.session_state.current_conversation
        
        # Scenario display
        with st.expander("📖 Scene Synopsis", expanded=False):
            st.write(conv["scenario"])
        
        # Conversation display
        st.subheader("💬 Dialogue")
        
        messages = conv.get("messages", [])
        
        if not messages:
            st.info("No messages yet - the scene is beginning...")
        else:
            # Single play button for entire scene audio
            if TTS_AVAILABLE:
                audio_file = _generate_combined_audio(messages)
                if audio_file and os.path.exists(audio_file):
                    st.audio(audio_file, format='audio/mp3')

            # Display character messages in a nice format
            for idx, msg in enumerate(messages):
                with st.chat_message(msg.get("speaker_name", "Unknown")):
                    st.write(msg["content"])
                    st.caption(f"_{msg.get('timestamp', 'just now')}_")
        
        st.divider()
        
        # User Interaction Option
        st.subheader("🎙️ Your Turn (Optional)")
        
        characters_in_scene = conv.get("character_names", [])
        speaking_char = st.selectbox(
            "Speak as which character?",
            characters_in_scene,
            key="sim_user_speaker"
        )
        user_message = st.text_input(
            "What would you like to say?",
            placeholder="Type your message or question...",
            key="sim_user_message_input"
        )
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💬 Say It", use_container_width=True):
                if user_message:
                    # Add user message to display
                    st.session_state.conversation_history.append({
                        "speaker": speaking_char,
                        "content": user_message,
                        "timestamp": datetime.now().isoformat()
                    })
                    # Get response from character
                    response = chat_with_character(speaking_char, user_message)
                    if response:
                        st.session_state.conversation_history.append({
                            "speaker": speaking_char,
                            "content": response,
                            "is_ai_response": True,
                            "timestamp": datetime.now().isoformat()
                        })
                    st.rerun()
    
    with col2:
        st.subheader("🎮 Controls")
        
        if st.button("💾 Save Scene", use_container_width=True):
            filename = save_conversation_locally()
            st.success(f"✅ Saved to {filename}")
        
        st.divider()
        
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("🔤 Info", use_container_width=True):
                st.session_state.current_screen = "characters"
                st.rerun()
        
        with col_nav2:
            if st.button("← Home", use_container_width=True):
                st.session_state.current_screen = "home"
                st.rerun()


def characters_info_screen():
    """Show detailed character information"""
    st.title("👥 Cast Information")
    st.markdown("Meet the TechStory team")
    
    st.divider()
    
    if st.session_state.current_conversation:
        conv = st.session_state.current_conversation
        character_names = conv.get("character_names", [])
    else:
        character_names = [c["name"] for c in st.session_state.characters]
    
    for char_name in character_names:
        char_data = next((c for c in st.session_state.characters if c["name"] == char_name), None)
        
        if char_data:
            with st.expander(f"👤 {char_data['name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Title:** {char_data.get('title', 'N/A')}")
                    st.markdown(f"**Gender:** {char_data.get('gender', 'N/A')}")
                    st.markdown(f"**Age:** {char_data.get('age', 'N/A')}")
                    st.markdown(f"**Born:** {char_data.get('birthdate', 'N/A')}")
                
                with col2:
                    traits = char_data.get('personality_traits', {})
                    st.markdown("**Personality Traits:**")
                    for trait, value in traits.items():
                        st.progress(value/100, text=f"{trait.title()}: {value}")
                
                st.markdown(f"**Personality:** {char_data.get('personality', 'N/A')}")
                st.markdown(f"**Backstory:** {char_data.get('backstory', 'N/A')}")
    
    if st.button("← Back"):
        st.session_state.current_screen = "simulation"
        st.rerun()


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    # Load characters on startup
    if not st.session_state.characters:
        with st.spinner("Loading TechStory cast..."):
            chars = load_characters()
            if chars:
                st.session_state.characters = chars
            else:
                st.error("Failed to load characters. Is the backend running?")
                st.stop()
    
    # Get sidebar controls for all screens
    if st.session_state.current_screen != "home":
        selected_chars, num_turns = sidebar_controls()
    
    # Navigation
    if st.session_state.current_screen == "home":
        home_screen()
    elif st.session_state.current_screen == "simulation":
        simulation_screen()
    elif st.session_state.current_screen == "characters":
        characters_info_screen()
    
    # Footer
    st.divider()
    st.caption(f"🎭 TechStory Theatre | Backend API: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
