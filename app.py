from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key from Render environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    print(f"User: {incoming_msg}")

    try:
        # Ask OpenAI GPT-3.5
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=incoming_msg,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        answer = "⚠️ AI system down. Try again later."

    # Send back via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(answer)
    return str(twilio_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
