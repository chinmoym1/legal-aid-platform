import streamlit as st
from langchain_community.chat_models import ChatOllama
from sentence_transformers import SentenceTransformer, util

# ---------------------------
# Initialize LLM
# ---------------------------
llm = ChatOllama(model="llama3", streaming=True)

# ---------------------------
# Define helper to get LLM output
# ---------------------------
def llm_complete(question: str) -> str:
    """Generate full answer from LLM (handles streaming)."""
    full_response = ""
    for chunk in llm.stream(question):
        full_response += chunk.content or ""
    return full_response

# ---------------------------
# Questions & Gold Answers
# ---------------------------
questions = [
    "What are the fundamental rights guaranteed by the Indian Constitution?",
    "Explain the significance of Article 21 in India.",
    "What is the process to get an Aadhaar card in India?",
    "Can a landlord increase rent without notice under Indian law?",
    "What was Article 370 and why was it repealed?",
    "What are the powers of the President of India under Article 356?",
    "Explain the difference between a public servant and a government employee.",
    "What rights do consumers have under the Consumer Protection Act, 2019?",
    "How is the Right to Education implemented in India?",
    "What are the major types of tenancy rights under Indian law?"
]

gold_answers = [
    "Fundamental rights include right to equality, freedom of speech, right against exploitation, right to freedom of religion, cultural rights, and right to constitutional remedies.",
    "Article 21 guarantees protection of life and personal liberty to every citizen and is interpreted broadly to include rights like privacy, health, and dignity.",
    "Aadhaar is obtained by visiting a UIDAI enrolment center, submitting ID and address proofs, and providing biometric data.",
    "It depends on lease terms and local laws; generally, landlords must provide notice unless otherwise specified by law.",
    "Article 370 gave J&K special status; it was repealed in 2019 to fully integrate the state with India.",
    "Article 356 allows the President to impose President's Rule in states under certain conditions when constitutional machinery fails.",
    "A public servant holds a position under the government and is subject to conduct rules; not all government employees are public servants.",
    "Consumers have the right to be protected against unfair trade practices, defective goods, and deficient services.",
    "Right to Education ensures free and compulsory education for children aged 6-14 years and mandates infrastructure and teacher quality.",
    "Tenancy rights include right to occupy, right to fair rent, protection against arbitrary eviction, and right to transfer tenancy in some cases."
]

# ---------------------------
# Load embedding model
# ---------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------
# Evaluate similarity
# ---------------------------
for q, gold in zip(questions, gold_answers):
    print(f"\nQ: {q}")
    llm_answer = llm_complete(q)
    sim_score = util.cos_sim(embedder.encode(llm_answer), embedder.encode(gold)).item()
    print(f"LLM Answer: {llm_answer[:200]}...")  # print first 200 chars
    print(f"Similarity Score: {sim_score:.3f}")

    #0.613, 0.705, 0.780, 0.501, 0.725, 0.533, 0.778, 0.684, 0.658, 0.654
'''Step-by-step calculation:

Sum:
0.613 + 0.705 = 1.318
1.318 + 0.780 = 2.098
2.098 + 0.501 = 2.599
2.599 + 0.725 = 3.324
3.324 + 0.533 = 3.857
3.857 + 0.778 = 4.635
4.635 + 0.684 = 5.319
5.319 + 0.658 = 5.977
5.977 + 0.654 = 6.631

Divide by number of questions (10):
6.631 ÷ 10 = 0.6631

✅ Average similarity score ≈ 0.66'''
