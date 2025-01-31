from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Use OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_titles(topic):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-site.com",  # Optional for ranking
        "X-Title": "Your App Name"  # Optional for ranking
    }

    prompt = f"""
    You are a creative YouTube title generator. Your task is to take the given YouTube video title and rewrite it into 10 viral, attention-grabbing, and click-worthy YouTube titles. The titles should be engaging, use power words, and appeal to a broad audience. Keep them concise and under 70 characters.

    Video Title: {topic}
    """

    data = {
        "model": "deepseek/deepseek-r1:free",  # Ensure this model is available on OpenRouter
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        try:
            content = response.json()["choices"][0]["message"]["content"]
            return [line.strip('- ') for line in content.split("\n") if line.strip()]
        except (KeyError, IndexError):
            return ["Error: Unexpected API response format"]
    return [f"Error: {response.status_code} - {response.text}"]

@app.route("/", methods=["GET", "POST"])
def index():
    titles = []
    topic = ""
    if request.method == "POST":
        topic = request.form.get("topic", "")
        if topic:
            titles = generate_titles(topic)
    return render_template("index.html", titles=titles, topic=topic)

if __name__ == "__main__":
    app.run(debug=True)
