from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load OpenAI key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        incoming_msg = request.values.get('Body', '').strip()

        # Get AI response using latest API (openai>=1.0.0)
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}],
            temperature=0.7
        )

        reply_text = response.choices[0].message.content.strip()

    except Exception as e:
        reply_text = "⚠️ AI system down hai. Try again later."

    # Twilio response
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply_text)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
