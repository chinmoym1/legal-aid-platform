# test_llm.py
import os
import traceback
from llm_providers import llm_complete

if __name__ == "__main__":
    # Force backend to hf-hub
    os.environ["LLM_BACKEND"] = "hf-hub"
    os.environ["HF_HUB_MODEL"] = "bigscience/bloom-560m"  # change if needed

    prompt = "What is the capital of France?"
    try:
        print(">>> Sending prompt to Hugging Face Hub...")
        response = llm_complete(prompt)
        print(">>> Response:", response)
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
