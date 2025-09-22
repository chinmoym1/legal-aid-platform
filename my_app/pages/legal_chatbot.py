# pages/chatbot.py
import streamlit as st
from langchain_community.chat_models import ChatOllama
from streamlit_mic_recorder import speech_to_text

def show_chatbot():
    st.title("⚖️ Legisense → intelligent, sensible advice")

    # Initialize LLM
    llm = ChatOllama(model="llama3")

    # Initialize chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # ---------- Sidebar: Chat History ----------
    with st.sidebar:
        st.title("📜 Chat History")
        if st.session_state.history:
            for i, chat in enumerate(st.session_state.history, 1):
                with st.expander(f"Chat {i}"):
                    st.markdown(f"**🧑 You:** {chat['question']}")
                    st.markdown(f"**🤖 Bot:** {chat['answer']}")
        else:
            st.info("No history yet. Ask something!")

    # ---------- Main Chat UI ----------
    col1, col2 = st.columns([8, 1])

    with col1:
        query = st.text_input("Ask a legal question...", key="user_input", label_visibility="collapsed")

    with col2:
        voice_query = speech_to_text(
            language="en",
            use_container_width=True,
            just_once=True,
            key="STT",
            start_prompt="🎤",
            stop_prompt="⏹️"
        )

    # Prefer mic input if available
    if voice_query:
        query = voice_query  

    # Handle query
    if query:
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            for chunk in llm.stream(query):
                token = chunk.content if chunk.content else ""
                full_response += token
                placeholder.markdown(full_response)

        st.session_state.history.append({"question": query, "answer": full_response})
