from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        if incoming_msg:
            # OpenAI GPT call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            reply = response['choices'][0]['message']['content'].strip()
            msg.body(reply)
        else:
            msg.body("❌ Empty message received.")
    except Exception as e:
        msg.body("⚠️ AI system down hai. Try again later.")
        print(f"OpenAI Error: {e}")  # Logs me dikhega

    return str(resp)
