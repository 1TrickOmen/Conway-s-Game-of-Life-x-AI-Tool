# api/main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import sys
import os

# Add parent directory to path so we can import game_of_life
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the current directory (api/) to Python's path so it can find game_of_life.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_of_life import run_until_stable
app = FastAPI(title="Conway's Game of Life API")

class ResponseModel(BaseModel):
    word: str
    generations: int
    score: int
    final_state: str

@app.get("/conway", response_model=ResponseModel)
def conway(word: str = Query(..., min_length=1, max_length=50)):
    result = run_until_stable(word.strip())
    return {
        "word": word.lower(),
        "generations": result["generations"],
        "score": result["score"],
        "final_state": result["final_state"]
    }