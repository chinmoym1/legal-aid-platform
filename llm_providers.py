# llm_providers.py
"""
LLM Providers - Ollama only backend
Author: Rahul Manchanda
"""

import subprocess

# Change this to use a different Ollama model if needed
OLLAMA_MODEL = "llama3"


def _ollama_complete(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """
    Calls Ollama locally using subprocess and returns the model response.
    """
    try:
        # Run the ollama command
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
        )

        # Check for errors
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"[Ollama Error: {result.stderr}]"

    except Exception as e:
        return f"[Ollama Exception: {str(e)}]"


def llm_complete(prompt: str) -> str:
    """
    Main function to send a prompt to Ollama and get the response.
    """
    return _ollama_complete(prompt)


# Example test run
if __name__ == "__main__":
    test_prompt = "Hello Ollama! Can you explain what AI is in one sentence?"
    print(">>> Sending prompt to Ollama...")
    response = llm_complete(test_prompt)
    print(">>> Response:", response)

