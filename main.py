import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment!")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_message = request.form.get("Body")
    print(f"📩 User Message: {user_message}")  # Only user messages for debugging

    # Prepare Groq API request
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",  # latest working model
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"].strip()
    except KeyError:
        bot_reply = "⚠️ Sorry, I could not process that."
    except requests.exceptions.RequestException as e:
        bot_reply = f"⚠️ Request error: {e}"
    except Exception as e:
        bot_reply = f"⚠️ Unexpected error: {e}"

    # Twilio WhatsApp reply
    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
