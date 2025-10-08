# legal_summarizer.py

import streamlit as st
import asyncio
import sys
import os
import base64
from io import BytesIO
import docx2txt
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# --- 1. INITIAL SETUP AND CONFIGURATION ---

# FIX: Set the correct event loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Load environment variables and configure Gemini API
load_dotenv()
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    MODEL = "gemini-2.5-flash"
except Exception as e:
    st.error(f"Failed to configure Gemini API. Please check your GOOGLE_API_KEY. Error: {e}")
    st.stop()

# --- 2. BACKEND HELPER FUNCTIONS (No changes needed here) ---

def create_pdf_with_playwright(summary_text: str, language: str) -> BytesIO:
    # This function is already working well.
    font_map = {
        "English": "NotoSans-Regular.ttf", "Hindi": "NotoSansDevanagari-Regular.ttf",
        "Bengali": "NotoSansBengali-Regular.ttf", "Tamil": "NotoSansTamil-Regular.ttf",
        "Telugu": "NotoSansTelugu-Regular.ttf", "Gujarati": "NotoSansGujarati-Regular.ttf",
        "Kannada": "NotoSansKannada-Regular.ttf", "Malayalam": "NotoSansMalayalam-Regular.ttf",
        "Odia": "NotoSansOriya-Regular.ttf", "Punjabi": "NotoSansGurmukhi-Regular.ttf",
        "Urdu": "NotoSansArabic-Regular.ttf"
    }
    font_file = font_map.get(language, "NotoSans-Regular.ttf")
    font_path = os.path.abspath(os.path.join("fonts", font_file))
    try:
        with open(font_path, "rb") as f:
            font_data = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Unable to generate PDF for '{language}' as its font file is missing.")
        return BytesIO()
    summary_html = summary_text.replace('\n', '<br>')
    html_content = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Legal Summary</title><style>
    @font-face {{ font-family: 'CustomFont'; src: url(data:font/truetype;charset=utf-8;base64,{font_data}) format('truetype'); }}
    body {{ font-family: 'CustomFont', sans-serif; font-size: 12pt; line-height: 1.6; margin: 40px; text-align: justify; }}
    h1 {{ text-align: center; font-size: 16pt; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
    </style></head><body><h1>Legal Summary ({language})</h1><p>{summary_html}</p></body></html>
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content)
            pdf_bytes = page.pdf(format="A4")
            browser.close()
        return BytesIO(pdf_bytes)
    except Exception as e:
        st.error(f"An error occurred during PDF generation with Playwright: {e}")
        return BytesIO()

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

def summarize_with_gemini(text: str, language: str) -> str:
    prompt = f"""
    You are an expert legal assistant. Summarize the following legal document into clear, simple, and easy-to-understand {language}.
    Focus on these key points and use them as bold headings in your response:
    1.  **Core Subject:** What is this document about in one sentence?
    2.  **Key Parties Involved:** Who are the main individuals or entities?
    3.  **Main Arguments or Decisions:** What are the central claims or judicial decisions made?
    4.  **Final Outcome:** What was the conclusion or result?

    Ensure the entire summary is written in the native script for {language}.
    Document Text: --- {text} ---
    """
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the AI model: {e}")
        return "Error: Could not generate summary."

# --- 3. REDESIGNED STREAMLIT UI ---
def show_legal_summarizer():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>📑 AI Legal Summarizer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload a dense legal document and our AI will distill it into a simple, easy-to-understand summary in your chosen language.</p>", unsafe_allow_html=True)
    st.divider()

    # --- Two-Column Layout ---
    col1, col2 = st.columns([1, 1.2]) # Input column is slightly smaller

    # --- COLUMN 1: CONTROLS & UPLOAD ---
    with col1:
        st.subheader("1. Configure Your Summary")
        selected_language = st.selectbox(
            "Choose summary language:",
            ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Gujarati", "Kannada", "Malayalam", "Odia", "Punjabi", "Urdu"]
        )

        st.subheader("2. Upload Your Document")
        uploaded_file = st.file_uploader(
            "Upload a legal document (PDF, DOCX, or TXT | Max 10MB)",
            type=["pdf", "docx", "txt"],
        )

        # --- NEW: FILE SIZE VALIDATION LOGIC ---
        MAX_FILE_SIZE_MB = 10
        if uploaded_file:
            file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)

            if file_size_mb > MAX_FILE_SIZE_MB:
                st.error(f"❌ File is too large ({file_size_mb:.2f} MB). Please upload a file smaller than {MAX_FILE_SIZE_MB} MB.")
            else:
                st.success(f"✅ File '{uploaded_file.name}' accepted ({file_size_mb:.2f} MB).")
                # The "Generate Summary" button only appears for valid files.
                if st.button("✨ Generate Summary", use_container_width=True, type="primary"):
                    with st.spinner("🤖 Analyzing and summarizing your document..."):
                        text = extract_text(uploaded_file)
                        if not text or not text.strip():
                            st.error("❌ Could not extract any readable text from the document.")
                        else:
                            summary = summarize_with_gemini(text, selected_language)
                            st.session_state['summary'] = summary
                            st.session_state['language'] = selected_language
                            st.rerun()

    # --- COLUMN 2: SUMMARY DISPLAY ---
    with col2:
        st.subheader("3. View Your Summary")
        if 'summary' in st.session_state:
            with st.container(border=True):
                st.markdown(f"#### Summary in {st.session_state['language']}")
                st.markdown(st.session_state['summary'])

                pdf_file = create_pdf_with_playwright(st.session_state['summary'], st.session_state['language'])
                if pdf_file.getbuffer().nbytes > 0:
                    st.download_button(
                        label="⬇️ Download Summary as PDF",
                        data=pdf_file,
                        file_name=f"Legal_Summary_{st.session_state['language']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            with st.container(border=True, height=300):
                st.info("Your document summary will appear here once generated.")