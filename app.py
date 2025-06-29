from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load OpenAI key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Keyword-based replies
    if "demo x1" in incoming_msg:
        msg.body("📽️ Alkafresh X1 Demo Video: https://youtu.be/demo_x1")
    elif "error e3" in incoming_msg:
        msg.body("🛠️ Error E3 – Water Flow Sensor Problem:\n1. Power off karein\n2. Pipe connection check karein\n3. Technician ko call karein: +91-99999-12345")
    elif "warranty" in incoming_msg or "af2023x1001" in incoming_msg:
        msg.body("✅ Serial No: AF2023X1001\n📅 Purchase Date: 15-Jun-2023\n🔒 Warranty Till: 15-Jun-2026")
    elif "technician" in incoming_msg:
        msg.body("📞 Technician Number: +91-99999-12345\n🕑 Timing: 10am – 6pm (Mon–Sat)")
    else:
        # AI fallback using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # You can use "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": "You are Alkafresh SmartCare WhatsApp support assistant. Reply in Hinglish."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            reply = response['choices'][0]['message']['content']
            msg.body(reply)
        except Exception as e:
            msg.body("⚠️ Sorry, AI system response failed. Try again later.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
