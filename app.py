from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# OpenAI config
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip()
    resp = MessagingResponse()

    if not incoming_msg:
        resp.message("❌ Empty message.")
        return str(resp)

    try:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful assistant for Alkafresh customer support."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        resp.message(reply)
    except Exception as e:
        print("AI Error:", e)
        resp.message("⚠️ AI system down hai. Try again later.")

    return str(resp)
