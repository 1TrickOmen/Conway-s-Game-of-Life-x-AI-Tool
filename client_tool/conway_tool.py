# client_tool/conway_tool.py
import requests
import random
import string
import os

# Set the URL of your running Conway API
CONWAY_API_URL = os.getenv("CONWAY_API_URL", "http://localhost:8000/conway")

def call_conway_api(word: str) -> dict:
    """Call the Conway API and return parsed JSON."""
    try:
        response = requests.get(CONWAY_API_URL, params={"word": word}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_generations_for_word(word: str) -> dict:
    """
    Tool for: 'How many generations will the word ‘monument’ return?'
    """
    result = call_conway_api(word)
    if "error" in result:
        return {"error": result["error"]}
    return {
        "word": result["word"],
        "generations": result["generations"]
    }

def generate_random_words_and_find_highest_score() -> dict:
    """
    Tool for: 'Generate 3 random words and tell me the highest Conway score.'
    """
    def random_word():
        # Generate a random word of 3–8 lowercase letters
        length = random.randint(3, 8)
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    # Generate 3 random words
    words = [random_word() for _ in range(3)]
    results = []

    for w in words:
        res = call_conway_api(w)
        if "error" not in res:
            results.append({"word": w, "score": res["score"]})

    # Find the highest score
    if results:
        best = max(results, key=lambda x: x["score"])
        return {
            "generated_words": [r["word"] for r in results],
            "highest_scoring_word": best["word"],
            "highest_score": best["score"]
        }
    else:
        return {"error": "Failed to get scores for random words"}

# === TOOL SCHEMA FOR OPENAI ===
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_generations_for_word",
            "description": "Get the number of generations until stability for a given word in Conway's Game of Life simulation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The input word (e.g., 'monument')"
                    }
                },
                "required": ["word"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_random_words_and_find_highest_score",
            "description": "Generate 3 random words and determine which has the highest Conway Game of Life spawn score.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]