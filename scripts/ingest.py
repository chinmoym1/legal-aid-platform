"""
Ingestion Script
Author: Rahul Manchanda
"""

import os
import glob
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# ---------------------------
# Configuration
# ---------------------------
RAW_DIR = "data/raw"
INDEX_DIR = "data/index"
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

os.makedirs(INDEX_DIR, exist_ok=True)

# ---------------------------
# Collect TXT Files
# ---------------------------
all_files = glob.glob(f"{RAW_DIR}/**/*.txt", recursive=True)
print(f"Found {len(all_files)} TXT files to process.")

# ---------------------------
# Load and Chunk Documents
# ---------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    length_function=len
)

docs = []
for file_path in all_files:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    chunks = text_splitter.split_text(text)
    docs.extend([Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks])

print(f"Created {len(docs)} document chunks.")

# ---------------------------
# Embeddings
# ---------------------------
embedding = HuggingFaceEmbeddings(model_name=MODEL_NAME)

# ---------------------------
# Build FAISS Index
# ---------------------------
vectorstore = FAISS.from_documents(docs, embedding)
vectorstore.save_local(INDEX_DIR)

print("✅ FAISS index and metadata saved successfully at:", INDEX_DIR)

