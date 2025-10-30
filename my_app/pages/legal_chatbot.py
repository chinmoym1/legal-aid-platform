# pages/legal_chatbot.py
# --- This file should be inside your 'pages/' folder ---

import streamlit as st
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai
from dotenv import load_dotenv
import os

# --- PAGE CONFIGURATION AND API SETUP ---

# --- Page Config ---
# Set page config as the first Streamlit command
try:
    st.set_page_config(page_title="AI Legal Assistant", page_icon="🤖", layout="wide")
except st.errors.StreamlitAPIException:
    # Already set on home page
    pass

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    # We should show this error on the page, not just the console
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY in your .env file.")
    st.stop()


# --- CUSTOM STYLING (CSS) ---
def load_css():
    """Injects custom CSS to match the professional theme."""
    st.markdown("""
        <style>
            /* --- 1. FONT & COLOR PALETTE (Same as Home) --- */
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&family=Lato:wght@300;400;700&display=swap');
            
            :root {
                --font-serif: 'EB Garamond', serif;
                --font-sans: 'Lato', sans-serif;
                --color-primary-dark: #001F3F; /* Deep Navy */
                --color-primary-light: #003B73;
                --color-accent-gold: #B8860B;   /* Muted Gold */
                --color-bg-light: #FDFBF6;      /* Warm off-white */
                --color-bg-dark: #F4F4F4;       /* Light grey */
                --color-text-dark: #2F2F2F;     /* Charcoal */
                --color-text-light: #666666;
                --color-white: #FFFFFF;
                --color-border: #DDDDDD;
            }

            /* --- 2. GLOBAL STYLES --- */
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                font-family: var(--font-sans);
                background-color: var(--color-bg-light);
                color: var(--color-text-dark);
            }
            [data-testid="stHeader"] { display: none; }
            
            /* Add padding to bottom to avoid st.chat_input overlap */
            [data-testid="stAppViewContainer"] {
                padding-bottom: 7rem;
            }
            
            /* --- 3. CHAT PAGE HEADER --- */
            .chat-header {
                font-family: var(--font-serif);
                font-size: 2.75rem; /* 44px */
                font-weight: 600;
                color: var(--color-primary-dark);
                text-align: center;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
            }
            .chat-subheader {
                text-align: center;
                font-size: 1.1rem;
                color: var(--color-text-light);
                margin-bottom: 2rem;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.6;
            }

            /* --- 4. CHAT MESSAGE BUBBLES (Using YOUR original classes) --- */
            .chat-bubble {
                padding: 1rem;
                border-radius: 20px;
                margin-bottom: 10px;
                max-width: 75%;
                display: inline-block;
                clear: both;
                line-height: 1.6;
                /* Add a little space for the avatar */
                padding-left: 3rem;
                position: relative;
            }
            .chat-bubble-avatar {
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 1.5rem;
            }

            .user-bubble {
                background-color: var(--color-primary-dark);
                color: var(--color-white);
                float: right;
                border-bottom-right-radius: 5px;
            }
            .assistant-bubble {
                background-color: var(--color-white);
                color: var(--color-text-dark);
                border: 1px solid var(--color-border);
                float: left;
                border-bottom-left-radius: 5px;
            }
            
            /* Container for messages to clear floats */
            .message-container {
                clear: both;
                overflow: auto; /* Ensures the container expands to fit floats */
                padding: 0 1rem; /* Add some horizontal padding */
            }


            /* --- 5. WELCOME SCREEN & EXAMPLE PROMPTS --- */
            .welcome-title {
                font-family: var(--font-serif);
                font-size: 2rem;
                font-weight: 500;
                color: var(--color-text-dark);
                text-align: center;
                margin-bottom: 1.5rem;
            }
            
            /* Style the st.button for example prompts */
            [data-testid="stButton"] > button {
                background-color: var(--color-white);
                color: var(--color-primary-dark);
                border: 1px solid var(--color-border);
                border-radius: 8px;
                padding: 12px 18px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            [data-testid="stButton"] > button:hover {
                background-color: var(--color-white);
                color: var(--color-accent-gold);
                border-color: var(--color-accent-gold);
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                transform: translateY(-2px);
            }
            [data-testid="stButton"] > button:active {
                background-color: var(--color-bg-dark) !important;
            }

            /* --- 6. SIDEBAR BUTTON --- */
            [data-testid="stSidebar"] [data-testid="stButton"] > button {
                background: #FFFBEB; /* Light yellow from disclaimer */
                color: #B45309; /* Amber text */
                border: 1px solid #F59E0B;
                font-weight: 700;
            }
            [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
                background: #FEF3C7;
                border-color: #B45309;
                color: #92400E;
            }

            /* --- 7. CHAT INPUT BAR --- */
            /* This is the outer container */
            /*[data-testid="stChatInput"] {
                background-color: var(--color-bg-light); /* Match the page BG */
                border-top: 1px solid var(--color-border); /* Keep the top line separator */
                border-left: none;
                border-right: none;
                border-bottom: none;
                box-shadow: none; */ /* Remove any default shadow */
            }
            /* This is the inner text area */
            [data-testid="stChatInput"] textarea {
                background-color: var(--color-white);
                color: var(--color-text-dark);
                border-radius: 8px;
                border: 1px solid var(--color-border);
            }
            [data-testid="stChatInput"] textarea:focus {
                border-color: var(--color-accent-gold);
                box-shadow: none;
            }

            /* --- 8. VOICE RECORDER BUTTON --- */
            /* This targets the mic button from streamlit_mic_recorder */
            button[title="🎤 Ask with Voice"], button[title="⏹️ Stop recording"] {
                background-color: var(--color-primary-dark) !important;
                color: var(--color-white) !important;
                border-radius: 8px !important;
                width: 50px !important; /* Make it a square */
                height: 50px !important;
                margin-top: 2px; /* Align with chat input */
                transition: background-color 0.3s ease;
            }
            button[title="🎤 Ask with Voice"]:hover {
                background-color: var(--color-primary-light) !important;
            }
            button[title="⏹️ Stop recording"] {
                background-color: var(--color-accent-gold) !important;
            }

        </style>
    """, unsafe_allow_html=True)

def show_chatbot():
    """Main function to display the chatbot page."""
    
    load_css()

    st.markdown("<div class='chat-header'>🤖 AI Legal Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-subheader'>Ask any legal question. I'm here to provide preliminary guidance. Please note, I am an AI and not a substitute for a qualified lawyer.</div>", unsafe_allow_html=True)
    
    # --- Initialize Chat Session ---
    if "chat" not in st.session_state:
        # Updated system prompt for a more professional tone
        system_prompt = (
            "You are an expert AI legal assistant. Your purpose is to provide general legal "
            "information, analysis, and document guidance. Your responses MUST be objective, "
            "concise, and professional. Use bullet points for lists. "
            "Your entire response MUST NOT EXCEED 150 words. This is a hard rule."
            "You are not a lawyer and cannot provide legal advice."
            "Your entire response, including the disclaimer, should be clear and easy to understand."
        )
        try:
            model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_prompt)
            st.session_state.chat = model.start_chat(history=[])
        except Exception as e:
            st.error(f"Failed to initialize the generative model: {e}")
            st.stop()
            
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Sidebar for Chat Controls ---
    with st.sidebar:
        st.title("📜 Chat Controls")
        if st.button("Clear Chat History", use_container_width=True, key="clear_chat"):
            st.session_state.messages = []
            st.session_state.pop("chat", None) # Reset the chat model session
            st.rerun()

    # --- Display Welcome Screen (if no messages) ---
    if not st.session_state.messages:
        st.markdown("<div class='welcome-title'>How can I help you today?</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What are the steps to file an RTI?", use_container_width=True):
                st.session_state.example_prompt = "What are the steps to file an RTI?"
        with col2:
            if st.button("Explain 'breach of contract'", use_container_width=True):
                st.session_state.example_prompt = "Explain 'breach of contract'"
        with col3:
            if st.button("What is a Public Interest Litigation (PIL)?", use_container_width=True):
                st.session_state.example_prompt = "What is a Public Interest Litigation (PIL)?"

    # --- Display Chat History (Using YOUR original logic) ---
    st.markdown("<div class='message-container'>", unsafe_allow_html=True) # Container to help with floats
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        # Use your original class logic
        bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
        avatar = "🧑" if role == "user" else "🤖"
        
        # We'll add the avatar manually
        st.markdown(f'''
            <div class="chat-bubble {bubble_class}">
                <span class="chat-bubble-avatar">{avatar}</span>
                {content}
            </div>
        ''', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # --- Handle API Call if new user message exists ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_user_message = st.session_state.messages[-1]["content"]
        with st.spinner("Thinking... 🧠"):
            try:
                generation_config = {"max_output_tokens": 1024}
                response = st.session_state.chat.send_message(last_user_message, generation_config=generation_config)
                
                if response.parts:
                    answer = response.text.strip()
                else:
                    answer = "I'm sorry, I couldn't generate a response for that. Please try rephrasing your question."
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
                st.session_state.messages.pop() # Remove the user message if API fails


    # --- VOICE AND TEXT INPUT SECTION ---
    # Use columns to place the text bar and voice button side-by-side
    col_text, col_mic = st.columns([0.85, 0.15]) # 85% for text, 15% for mic

    with col_text:
        prompt = st.chat_input("Type your legal question here...")

    with col_mic:
        # We need to add a small amount of CSS to align the mic button
        st.markdown("""
        <style>
            div[data-testid="column"]:has(button[title="🎤 Ask with Voice"]) {
                display: flex;
                justify-content: center;
                align-items: center;
                padding-top: 10px; /* Adjust as-needed */
            }
        </style>
        """, unsafe_allow_html=True)
        
        voice_query = speech_to_text(
            language="en",
            use_container_width=True,
            just_once=True,
            key="STT",
            start_prompt="🎤",
            stop_prompt="⏹️",
        )

    # --- Combine input sources and trigger rerun ---
    final_prompt = prompt or voice_query or st.session_state.get("example_prompt")

    if final_prompt:
        st.session_state.pop("example_prompt", None) # Clear example prompt
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        st.rerun()

# --- Main execution ---
# This check ensures this code runs when the script is executed directly
# or as a Streamlit page
if __name__ == "__main__":
    show_chatbot()

