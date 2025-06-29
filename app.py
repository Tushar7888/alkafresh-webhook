from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("❌ Message empty hai. Type something.")
        return str(resp)

    try:
        # OpenAI call
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant for Alkafresh SmartCare. Reply in Hinglish."},
                {"role": "user", "content": incoming_msg}
            ]
        )

        reply = ai_response.choices[0].message.content.strip()
        msg.body(reply)

    except Exception as e:
        print("OpenAI Error:", e)
        msg.body("⚠️ AI system down hai. Please try again later.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

