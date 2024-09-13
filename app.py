from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model and chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Predefined Q&A pairs for quick responses
predefined_answers = {
    "What do you do": "I help people plan trips.",
    "What is your purpose": "I am an AI-based trip advisor.",
    " ": "To get a visa for Australia, apply online through the Australian Government's Department of Home Affairs website.",
    "What is the best way to travel around Europe?": "Traveling by train is often the best way. Consider getting a Eurail pass.",
    "What are some tips for budget travel?": "Book flights early, stay in hostels, use public transport, and eat locally."
}

def clean_text(text):
    """Clean the text by removing markdown symbols and extra whitespace."""
    text = text.replace('**', '')  # Remove bold markers
    text = text.strip()  # Remove any leading or trailing whitespace 
    return text

def format_response(source, message):
    """Format the response to be returned in JSON format."""
    return {
        'source': source,
        'message': clean_text(message)
    }

def get_gemini_response(question):
    """Get a response from Gemini model or use predefined answers.""" 
    # Check if the question has a predefined answer
    if question in predefined_answers:
        return format_response('Predefined', predefined_answers[question])
    
    try:
        # Request a response from the Gemini model
        response = chat.send_message(question, stream=False)
        response_text = response.text if response else "I'm sorry, I couldn't get an answer."
        return format_response('Gemini', response_text)
    except Exception as e:
        print(f"Error getting response from Gemini model: {e}")
        return format_response('Error', "I'm sorry, something went wrong while trying to fetch the answer.")

app = Flask(__name__)

@app.route('/')
def home():
    """Render the homepage with the chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_route():
    """Handle chat messages from users."""
    user_input = request.json.get('message')
    if user_input:
        response = get_gemini_response(user_input)
        return jsonify(response)
    return jsonify({"source": "Error", "message": "No input provided."})

if __name__ == "__main__":
    # Run the Flask app on port 6789
    app.run(debug=True, port=6789)
