"""
Core RAG Pipeline (Updated)
Author: Rahul Manchanda
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA

# ---------------------------
# Configuration
# ---------------------------
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
INDEX_DIR = "data/index"

# ---------------------------
# Load Embeddings + Vectorstore
# ---------------------------
embedding = HuggingFaceEmbeddings(model_name=MODEL_NAME)

vectorstore = FAISS.load_local(
    INDEX_DIR,
    embeddings=embedding,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ---------------------------
# LLM Setup
# ---------------------------
llm = ChatOllama(model="llama3", temperature=0)

# ---------------------------
# RAG Chain
# ---------------------------
prompt_template = ChatPromptTemplate.from_template("""
You are a legal assistant for Indian citizens.
Use the following retrieved documents to answer the question.
If the answer is not in the documents, say "I don’t know based on the available legal documents."

Context:
{context}

Question:
{question}

Answer as a helpful legal advisor:
""")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template}
)

# ---------------------------
# Query Function
# ---------------------------
def query_bot(question: str) -> str:
    response = qa_chain.invoke({"query": question})
    return response["result"]

# ---------------------------
# Test Run
# ---------------------------
if __name__ == "__main__":
    test_q = "What are the rights of a tenant under Indian law?"
    print(">> Querying bot...")
    print(query_bot(test_q))
