from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model and chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Expanded predefined Q&A pairs for Indian travel
predefined_answers = {
    "What is the best time to visit India?": "The best time to visit India is generally from October to March.",
    "What are the must-see attractions in India?": "Must-see attractions include the Taj Mahal, Jaipur's forts, Kerala's backwaters, and Goa's beaches.",
    "How do I get a visa for India?": "Apply online through the Indian Government's e-Visa portal or visit an Indian embassy/consulate.",
    "What is the best way to travel around India?": "Travel by train using Indian Railways or consider domestic flights for long distances.",
    "What are some tips for budget travel in India?": "Travel by trains or buses, stay in budget hotels, and eat at local eateries."
}

def is_indian_travel_related(question):
    """Determine if the question pertains to Indian travel."""
    indian_travel_keywords = [
        "India", "Indian", "Delhi", "Mumbai", "Goa", "Jaipur", "Kerala", "Taj Mahal", "e-Visa",
        "Indian Railways", "Agra", "Varanasi", "Rajasthan", "Shimla", "Manali", "Udaipur",
    ]
    return any(keyword.lower() in question.lower() for keyword in indian_travel_keywords)

def clean_text(text):
    """Remove unnecessary characters from text."""
    text = text.replace('*', '').replace('_', '').replace('`', '').strip()
    return text

def format_gemini_response(response_text):
    """Format the Gemini response for improved readability."""
    clean_response = clean_text(response_text)
    formatted_response = (
        f"**Response from Gemini:**\n\n"
        f"- **Here is the information you requested:**\n\n"
        f"  {clean_response}\n\n"
        f"- **If you need more details, please let me know!**\n"
    )
    return formatted_response

def generate_answer(question):
    """Generate an answer based on the question."""
    question = clean_text(question)
    if is_indian_travel_related(question):
        # Check for predefined answers first
        for q, a in predefined_answers.items():
            if question.lower() == q.lower():
                return format_gemini_response(a)
        
        # Generate an answer using the Gemini Pro model
        try:
            response = chat.send_message(question, stream=False)
            response_text = response['text'] if response else "I'm sorry, I couldn't get an answer."
            return format_gemini_response(response_text) 
        except Exception as e:
            print(f"Error getting response from Gemini model: {e}")
            return format_gemini_response("I'm sorry, something went wrong while trying to fetch the answer.")
    else:
        return "Sorry, I have no idea regarding the query."

# Example usage
if __name__ == "__main__":
    user_question = input("Ask a question about traveling in India: ")
    print(generate_answer(user_question))
