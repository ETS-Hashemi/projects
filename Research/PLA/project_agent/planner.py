import openai
import os

# Explicitly set the API key (this avoids all proxy-related issues)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_next_steps(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Python AI research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=800
    )
    return response.choices[0].message.content
