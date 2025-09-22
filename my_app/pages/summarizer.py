import streamlit as st
import subprocess
import tempfile
import re
import docx2txt

def show_legal_summarizer():
    st.title("📑 Legal Summarizer")
    st.write(
        "Upload a **judgment, contract, or legal document** and LegiSense will "
        "summarize it into simple, layman-friendly language."
    )

    # --------------------------
    # 📂 File Upload
    # --------------------------
    uploaded_file = st.file_uploader(
        "Upload a legal document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"]
    )

    # --------------------------
    # 📄 Extract Text
    # --------------------------
    def extract_text(file):
        if file.name.endswith(".pdf"):
            import PyPDF2
            reader = PyPDF2.PdfReader(file)
            return " ".join([page.extract_text() or "" for page in reader.pages])
        elif file.name.endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(file.read())
                return docx2txt.process(tmp.name)
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        return ""

    # --------------------------
    # 🦙 Call Ollama LLaMA 3
    # --------------------------
    def summarize_with_llama3(text: str) -> str:
        prompt = f"""
        Summarize the following legal judgment/contract in **layman’s terms**.
        Focus on:
        1. What the case/document is about
        2. The main issue
        3. The final decision/outcome (if any)

        Document:
        {text}
        """
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3"],
                input=prompt,
                text=True,
                stdout=subprocess.PIPE,     # ✅ capture clean output
                stderr=subprocess.DEVNULL   # ✅ silence spinner garbage
            )
            output = result.stdout.strip()

            # remove ANSI escape sequences (just in case)
            clean_output = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", output)

            if not clean_output:
                return "⚠️ No summary generated. Check if Ollama is running."

            return clean_output
        except Exception as e:
            return f"⚠️ Exception: {str(e)}"

    # --------------------------
    # 🚀 Run Summarization
    # --------------------------
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        if st.button("Summarize Document"):
            with st.spinner("🤖 LegiSense is summarizing..."):
                text = extract_text(uploaded_file)
                if not text.strip():
                    st.error("❌ No text could be extracted from the file.")
                else:
                    summary = summarize_with_llama3(text)
                    st.subheader("📌 Summary (Layman’s Terms)")
                    st.write(summary)
