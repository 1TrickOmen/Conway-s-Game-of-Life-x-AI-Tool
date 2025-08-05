# ui/app.py
import streamlit as st
from openai import OpenAI
import os
import sys
from pathlib import Path

# Add the project root to Python path so we can import client_tool
project_root = Path(__file__).parent.parent  # Go up from ui/ to root
sys.path.append(str(project_root))

# Now we can import from client_tool
try:
    from client_tool.conway_tool import TOOL_SCHEMAS, get_generations_for_word, generate_random_words_and_find_highest_score
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"  # ← REPLACE THIS!
client = OpenAI()

# UI
st.title("🧠 AI + Conway’s Game of Life Tool")
st.write("Ask any question. The AI can use the Conway simulation tool when needed.")

prompt = st.text_area("Enter your prompt:", height=100, placeholder="e.g., How many generations for 'hello'?")

if st.button("Ask AI"):
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("AI is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    tools=TOOL_SCHEMAS,
                    tool_choice="auto"
                )
                message = response.choices[0].message

                if message.tool_calls:
                    available_functions = {
                        "get_generations_for_word": get_generations_for_word,
                        "generate_random_words_and_find_highest_score": generate_random_words_and_find_highest_score
                    }
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        function_to_call = available_functions[function_name]
                        try:
                            args = eval(tool_call.function.arguments) if tool_call.function.arguments else {}
                        except:
                            args = {}
                        result = function_to_call(**args)
                        st.success(f"🔧 Tool Result: {result}")
                else:
                    st.info(f"💬 AI: {message.content}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")