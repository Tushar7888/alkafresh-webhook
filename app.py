from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from Render environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip()
    print(f"User Message: {incoming_msg}")  # Debug log

    resp = MessagingResponse()
    msg = resp.message()

    try:
        if incoming_msg:
            # Send to OpenAI GPT
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Alkafresh SmartCare AI  Bot. Answer in Hinglish."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            reply = completion.choices[0].message.content.strip()
            print(f"AI Response: {reply}")  # Debug log
        else:
            reply = "Kuch toh likho bhai 😅"

        msg.body(reply)

    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        msg.body("⚠️ AI system down hai. Try again later.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
