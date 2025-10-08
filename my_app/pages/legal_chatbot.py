# pages/chatbot.py

import streamlit as st
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai
from dotenv import load_dotenv
import os

# --- PAGE CONFIGURATION AND API SETUP ---

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("Gemini API key not found. Please set it in your .env file.")
    st.stop()


# --- CUSTOM STYLING (CSS) ---
def load_css():
    st.markdown("""
        <style>
            /* Main chat container */
            .st-emotion-cache-1jicfl2 {
                padding-bottom: 5rem; /* Add padding to prevent input from overlapping messages */
            }

            /* Chat message styling */
            .chat-bubble {
                padding: 15px;
                border-radius: 20px;
                margin-bottom: 10px;
                max-width: 75%;
                display: inline-block;
                clear: both;
            }
            .user-bubble {
                background-color: #004AAD; /* Primary Blue */
                color: white;
                float: right;
                border-bottom-right-radius: 5px;
            }
            .assistant-bubble {
                background-color: #F0F2F6; /* Light Gray */
                color: #31333F; /* Charcoal Text */
                float: left;
                border-bottom-left-radius: 5px;
            }

            /* Welcome message and example prompts */
            .welcome-container {
                text-align: center;
                padding: 2rem;
            }
            .welcome-title {
                color: #004AAD;
                font-size: 2.5em;
                font-weight: bold;
            }
            .example-prompt {
                background-color: #F0F2F6;
                border: 1px solid #D1D5DB;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            .example-prompt:hover {
                background-color: #E1E8F0;
            }
            .st-emotion-cache-yd4u6l {
                margin-top: 12px;
            }
        </style>
    """, unsafe_allow_html=True)


# --- MAIN CHATBOT FUNCTION ---
# def show_chatbot():
#     load_css()

#     st.markdown("<h1 style='text-align: center; color: #004AAD;'>🤖 AI Legal Assistant</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center;'>Ask me any legal question. I'm here to provide preliminary guidance.</p>", unsafe_allow_html=True)
#     st.divider()

#     # --- SESSION STATE INITIALIZATION ---
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # --- SIDEBAR FOR HISTORY AND CONTROLS ---
#     with st.sidebar:
#         st.title("📜 Chat Controls")
#         if st.button("Clear Chat History", use_container_width=True):
#             st.session_state.messages = []
#             st.rerun()

#         st.divider()
#         st.subheader("Voice Input (English)")
#         voice_query = speech_to_text(
#             language="en", use_container_width=True, just_once=True, key="STT",
#             start_prompt="🎤 Start Recording", stop_prompt="⏹️ Stop Recording"
#         )
#         if voice_query:
#             # When voice is used, it will be processed as the new prompt
#             st.session_state.voice_prompt = voice_query

#     # --- DISPLAY CHAT HISTORY ---
#     for message in st.session_state.messages:
#         role = message["role"]
#         content = message["content"]
#         bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
#         avatar = "🧑" if role == "user" else "🤖"
#         st.markdown(f'<div class="chat-bubble {bubble_class}">{avatar} {content}</div>', unsafe_allow_html=True)


#     # --- WELCOME SCREEN & EXAMPLE PROMPTS ---
#     if not st.session_state.messages:
#         st.markdown("<div class='welcome-container'><p class='welcome-title'>How can I help you today?</p></div>", unsafe_allow_html=True)
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             if st.button("What are the steps to file an RTI?", use_container_width=True):
#                 st.session_state.example_prompt = "What are the steps to file an RTI?"
#         with col2:
#             if st.button("Explain 'breach of contract'", use_container_width=True):
#                 st.session_state.example_prompt = "Explain 'breach of contract'"
#         with col3:
#             if st.button("What is a Public Interest Litigation (PIL)?", use_container_width=True):
#                 st.session_state.example_prompt = "What is a Public Interest Litigation (PIL)?"

#     # --- CHAT INPUT AND PROCESSING ---
#     prompt = st.chat_input("Ask a legal question...")

#     # Check for prompts from different sources
#     final_prompt = prompt or st.session_state.get("voice_prompt") or st.session_state.get("example_prompt")

#     if final_prompt:
#         # Clear temporary prompts
#         st.session_state.pop("voice_prompt", None)
#         st.session_state.pop("example_prompt", None)

#         # Add user message to state and display it
#         st.session_state.messages.append({"role": "user", "content": final_prompt})
        
#         # Display the latest user message immediately
#         st.markdown(f'<div class="chat-bubble user-bubble">🧑 {final_prompt}</div>', unsafe_allow_html=True)

#         # Generate and display AI response
#         with st.spinner("Thinking... 🧠"):
#             try:
#                 model = genai.GenerativeModel("gemini-2.0-flash")
#                 # --- NEW PROMPT AND CONFIG FOR SHORTER RESPONSES ---
#                 # 1. We create a detailed prompt that instructs the AI on its behavior.
#                 structured_prompt = f"""
#                 **Role:** You are a concise AI legal assistant named Legaliser.
#                 **Objective:** Answer the user's legal query directly and succinctly.

#                 **Instructions:**
#                 - Keep your response under 150 words. This is a strict limit.
#                 - Get straight to the point. Do not use filler phrases like "Certainly, I can help with that." or "Of course."
#                 - If a question can be answered with a list, use bullet points.
#                 - Do not provide lengthy background information or disclaimers unless they are critical to the answer. Your main goal is brevity and clarity.

#                 **User's Query:** "{final_prompt}"
#                 """

#                 # 2. We set a hard token limit as a safeguard.
#                 generation_config = {
#                     "max_output_tokens": 400, # A token is ~4 characters. This is a safety net.
#                     "temperature": 0.7,
#                 }

#                 # 3. We pass both the prompt and the config to the model.
#                 response = model.generate_content(
#                     structured_prompt,
#                     generation_config=generation_config
#                 )
#                 # --- END OF NEW SECTION ---

#                 response = model.generate_content(final_prompt)
#                 answer = response.text.strip()
#                 st.session_state.messages.append({"role": "assistant", "content": answer})
#                 # Rerun to display the new assistant message in the main loop
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"⚠️ An error occurred: {str(e)}")
#                 # Optionally remove the user message if the API call fails
#                 st.session_state.messages.pop()


# --- MAIN CHATBOT FUNCTION ---
# def show_chatbot():
#     load_css()

#     st.markdown("<h1 style='text-align: center; color: #004AAD;'>🤖 AI Legal Assistant</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center;'>Ask me any legal question. I'm here to provide preliminary guidance.</p>", unsafe_allow_html=True)
#     st.divider()

#     # --- 1. Use a proper Chat Session ---
#     # We initialize the chat model and session in the Streamlit session state.
#     if "chat" not in st.session_state:
#         # --- 2. Create a stronger, more direct system prompt ---
#         system_prompt = (
#             "You are Legaliser, an expert AI legal assistant. Your responses MUST be concise. "
#             "GET STRAIGHT TO THE POINT. Do not use filler words or introductory phrases like 'Certainly' or 'Of course.' "
#             "Use bullet points for lists. "
#             "Your entire response MUST NOT EXCEED 150 words. This is a hard rule."
#         )
#         model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_prompt)
#         st.session_state.chat = model.start_chat(history=[])

#     # --- Sidebar for history and controls ---
#     with st.sidebar:
#         st.title("📜 Chat Controls")
#         if st.button("Clear Chat History", use_container_width=True):
#             st.session_state.messages = []
#             st.session_state.pop("chat", None) # Clear the chat session object
#             st.rerun()
#         st.divider()
#         # Voice input can remain here or be moved if desired
#         voice_query = speech_to_text(language="en", use_container_width=True, just_once=True, key="STT", start_prompt="🎤", stop_prompt="⏹️")
#         if voice_query:
#             st.session_state.voice_prompt = voice_query

#     # Display chat messages from history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
        
#     for message in st.session_state.messages:
#         role = message["role"]
#         content = message["content"]
#         bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
#         avatar = "🧑" if role == "user" else "🤖"
#         st.markdown(f'<div class="chat-bubble {bubble_class}">{avatar} {content}</div>', unsafe_allow_html=True)

#     # Welcome screen for new chats
#     if not st.session_state.messages:
#         st.markdown("<div class='welcome-container'><p class='welcome-title'>How can I help you today?</p></div>", unsafe_allow_html=True)

#     # Chat input and processing
#     prompt = st.chat_input("Ask a legal question...")
#     final_prompt = prompt or st.session_state.get("voice_prompt")

#     if final_prompt:
#         st.session_state.pop("voice_prompt", None)
#         st.session_state.messages.append({"role": "user", "content": final_prompt})
        
#         # Display user message immediately
#         st.markdown(f'<div class="chat-bubble user-bubble">🧑 {final_prompt}</div>', unsafe_allow_html=True)

#         with st.spinner("Thinking... 🧠"):
#             try:
#                 # --- 3. Set a much stricter token limit ---
#                 # 250 tokens is roughly 180 words, a good safety net for a 150-word goal.
#                 generation_config = {"max_output_tokens": 250}

#                 # Send the message to the chat session and get the response
#                 response = st.session_state.chat.send_message(
#                     final_prompt,
#                     generation_config=generation_config
#                 )
#                 answer = response.text.strip()
#                 st.session_state.messages.append({"role": "assistant", "content": answer})
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"⚠️ An error occurred: {str(e)}")
#                 st.session_state.messages.pop()


def show_chatbot():
    load_css()

    st.markdown("<h1 style='text-align: center; color: #004AAD;'>🤖 AI Legal Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me any legal question. I'm here to provide preliminary guidance.</p>", unsafe_allow_html=True)
    st.divider()

    # --- Initialize Chat Session ---
    if "chat" not in st.session_state:
        system_prompt = (
            "You are Legaliser, an expert AI legal assistant. Your responses MUST be concise. "
            "GET STRAIGHT TO THE POINT. Do not use filler words. Use bullet points for lists. "
            "Your entire response MUST NOT EXCEED 150 words. This is a hard rule."
        )
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_prompt)
        st.session_state.chat = model.start_chat(history=[])

    # --- Sidebar for Chat Controls ---
    with st.sidebar:
        st.title("📜 Chat Controls")
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("chat", None)
            st.rerun()
        # The voice input has been removed from here.

    # --- Display Chat History and Welcome Screen ---
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = []
        st.markdown("<div class='welcome-container'><p class='welcome-title'>How can I help you today?</p></div>", unsafe_allow_html=True)
        # Your example prompt buttons go here...
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What are the steps to file an RTI?", use_container_width=True): st.session_state.example_prompt = "What are the steps to file an RTI?"
        with col2:
            if st.button("Explain 'breach of contract'", use_container_width=True): st.session_state.example_prompt = "Explain 'breach of contract'"
        with col3:
            if st.button("What is a Public Interest Litigation (PIL)?", use_container_width=True): st.session_state.example_prompt = "What is a Public Interest Litigation (PIL)?"

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
        avatar = "🧑" if role == "user" else "🤖"
        st.markdown(f'<div class="chat-bubble {bubble_class}">{avatar} {content}</div>', unsafe_allow_html=True)


    # The API call is now triggered by the rerun if there's a new user message
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
                st.session_state.messages.pop()


    # --- VOICE AND TEXT INPUT SECTION ---
    # We create a container at the bottom for the inputs
    # Use columns to place the text bar and voice button side-by-side
    st.write("")  # Spacer
    st.markdown("<br>", unsafe_allow_html=True)

    col_text, col_mic = st.columns([8, 1])  # Adjust ratios to balance widths

    with col_text:
        prompt = st.chat_input("Type your legal question here...")

    with col_mic:
        st.markdown(
            """
            <style>
            div[data-testid="column"]:has(> div button[title="🎤 Ask with Voice"]) {
                display: flex;
                align-items: center;
                justify-content: flex-end;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        voice_query = speech_to_text(
            language="en",
            use_container_width=True,
            just_once=True,
            key="STT",
            start_prompt="🎤",
            stop_prompt="⏹️",
        )

    # Combine input sources
    final_prompt = prompt or voice_query or st.session_state.get("example_prompt")

    if final_prompt:
        st.session_state.pop("voice_prompt", None)
        st.session_state.pop("example_prompt", None)
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        st.rerun()


    