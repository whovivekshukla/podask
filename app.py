from flask import Flask, jsonify, request

# Import required modules
import os
from embedchain import App
import gunicorn

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

@app.route('/', methods=['GET']) 
def home():
    return jsonify({"message": "Welcome to PodAsk API"})

@app.route('/', methods=['POST'])  # Change method to 'POST'
def summarize():
    # Parse JSON data from request
    data = request.json
    
    # Extract YouTube video links and query from JSON
    youtube_links = data.get('youtube_links', [])
    query = data.get('query', None)
    
    # Check if both links and query are provided
    if not youtube_links or not query:
        return jsonify({'error': 'Both YouTube links and query are required.'}), 400
    
    # Embed online resources
    for link in youtube_links:
        bot.add(link, data_type='youtube_video')
    
    # Query the app for summarized takeaways
    summary = bot.query(query)
    
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
