```markdown
# Monument AI - SEGA Challenge Submission

## Overview
A RESTful implementation of Conway’s Game of Life that uses the ASCII binary representation of an English word as the seed pattern. The service is integrated with `gpt-4o-mini` as a generative AI tool and includes a user-friendly interface for natural language interaction.

## Features
- ✅ **REST API**: Accepts a word and returns generations to stability and total spawn score
- ✅ **CGoL Simulation**: 60×40 grid, centered binary seed, standard rules, cycle/extinction detection
- ✅ **AI Tool Integration**: Compatible with `gpt-4o-mini` via OpenAI function calling
- ✅ **User Interface**: Streamlit web app for submitting any prompt to the LLM + tool
- ✅ **Full Local Execution**: No external dependencies beyond OpenAI API key

## How to Run

### 1. Start the Conway API
```bash
uvicorn api.main:app --reload
```
Keep this running — it powers the simulation.

### 2. Test the AI Tool (Optional)
```bash
python client_tool/openai_client.py
```
This demonstrates GPT-4o-mini using your tool for two key prompts.

### 3. Launch the Web UI
```bash
streamlit run ui/app.py
```
Open your browser to interact with the AI via a simple web interface.

## Requirements
Install dependencies first:
```bash
pip install fastapi uvicorn numpy requests openai streamlit
```

## Configuration
- Set your OpenAI API key in `client_tool/openai_client.py` and `ui/app.py`
- The Conway API URL defaults to `http://localhost:8000/conway` 

## Tools Used
- **Python 3.11**, FastAPI, NumPy, Streamlit
- **OpenAI GPT-4o-mini** with function calling
- **AI-assisted coding**:Qwen and ChatGPT were used for code suggestions, debugging, and structure design.
- **All logic was reviewed, tested, and understood by me.** No code was used without verification.

This project demonstrates full-stack integration of simulation, API design, AI tooling, and UX — with transparency and attention to detail.
```
