import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("Missing DEEPSEEK_API_KEY environment variable.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

completion = client.chat.completions.create(
    extra_headers={
        # "HTTP-Referer": "test.py",  # Optional. Site URL for rankings on openrouter.ai.
        # "X-Title": "http://example.com",  # Optional. Site title for rankings on openrouter.ai.
    },
    model="deepseek/deepseek-r1",
    messages=[
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
)

print(completion.choices[0].message.content)
