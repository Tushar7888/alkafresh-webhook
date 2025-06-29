from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# OpenAI API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()

    if not incoming_msg:
        resp.message("❌ Empty message received.")
        return str(resp)

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Alkafresh customer queries."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = completion.choices[0].message.content
        resp.message(reply)

    except Exception as e:
        print(f"OpenAI Error: {e}")
        resp.message("⚠️ AI system down hai. Try again later.")

    return str(resp)
