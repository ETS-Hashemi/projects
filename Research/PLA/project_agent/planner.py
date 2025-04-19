from openai import OpenAI

client = OpenAI()

def generate_next_steps(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Python AI research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=800
    )
    return response.choices[0].message.content
