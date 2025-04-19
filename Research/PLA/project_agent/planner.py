import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_next_steps(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ✅ valid model name
        messages=[
            {"role": "system", "content": "You are a Python AI research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=800
    )
    return response['choices'][0]['message']['content']
