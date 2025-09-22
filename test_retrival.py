import faiss
import pickle
from sentence_transformers import SentenceTransformer

# ---------------------------
# Configuration
# ---------------------------
INDEX_DIR = "data/index"
EMBEDDING_MODEL = "all-mpnet-base-v2"
TOP_K = 5  # number of chunks to retrieve

# ---------------------------
# Load FAISS Index & Metadata
# ---------------------------
index = faiss.read_index(f"{INDEX_DIR}/faiss_index.bin")
with open(f"{INDEX_DIR}/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# ---------------------------
# Initialize Embedding Model
# ---------------------------
embedder = SentenceTransformer(EMBEDDING_MODEL)

# ---------------------------
# Query Function
# ---------------------------
def retrieve_chunks(query, top_k=TOP_K):
    query_emb = embedder.encode([query])
    D, I = index.search(query_emb, top_k)
    
    results = []
    for idx in I[0]:
        source = metadata[idx]["source"]
        with open(source, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        results.append({"source": source, "content": text[:500]})  # first 500 chars
    return results

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    query = "What is the punishment for theft under IPC?"
    results = retrieve_chunks(query)

    for i, r in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Source: {r['source']}")
        print(f"Content Preview: {r['content']}")
        print("-" * 80)



