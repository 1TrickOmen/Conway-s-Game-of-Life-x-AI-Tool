# client_tool/openai_client.py
from openai import OpenAI
import os
from conway_tool import TOOL_SCHEMAS, get_generations_for_word, generate_random_words_and_find_highest_score

# 🔑 Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"  # ← REPLACE THIS!

client = OpenAI()

def run_prompt(prompt: str):
    print(f"\n💬 User: {prompt}")
    
    # Call GPT-4o-mini with tool capability
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        tools=TOOL_SCHEMAS,
        tool_choice="auto"  # Let GPT decide when to use tools
    )

    message = response.choices[0].message

    # Check if GPT wants to call a tool
    if message.tool_calls:
        available_functions = {
            "get_generations_for_word": get_generations_for_word,
            "generate_random_words_and_find_highest_score": generate_random_words_and_find_highest_score
        }
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            
            # Parse arguments (safe eval for simple cases)
            try:
                args = eval(tool_call.function.arguments) if tool_call.function.arguments else {}
            except:
                args = {}
            
            # Call the function
            result = function_to_call(**args)
            print(f"🤖 Assistant (via tool): {result}")
            return result
    else:
        # GPT answered directly
        print(f"🤖 Assistant: {message.content}")
        return {"llm_response": message.content}

# === Test the two required prompts ===
if __name__ == "__main__":
    run_prompt("How many generations will the word 'monument' return from the Conway tool?")
    run_prompt("Generate 3 random words and tell me the highest Conway score.")