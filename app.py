from flask import Flask, jsonify

# Import required modules
import os
from embedchain import App

app = Flask(__name__)

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"]
groq_api_key = os.environ["groq_api_key"]

config = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "Llama3-70b-8192",
            "api_key": groq_api_key,
            "stream": True
        }
    }
}

# Create a bot instance
bot = App.from_config(config=config)

# Embed online resources
bot.add('https://www.youtube.com/watch?v=w6qRb171cog', data_type='youtube_video')
bot.add('https://www.youtube.com/watch?v=y6NfxiemvHg', data_type='youtube_video')

# Define a route for summarization
@app.route('/', methods=['GET'])  # Add methods parameter with 'GET'
def summarize():
    # Query the app for summarized takeaways
    summary = bot.query("what did jensen huang talk about? summarise in 500 words")
    return summary

if __name__ == '__main__':
    app.run(debug=True)

