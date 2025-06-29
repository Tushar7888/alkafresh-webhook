from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Set up OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Check for keywords and respond
    if "demo x1" in incoming_msg:
        msg.body("📽️ Alkafresh X1 Demo Video: https://youtu.be/demo_x1")
    elif "error e3" in incoming_msg:
        msg.body("🔧 Error E3 – Water Flow Sensor Problem\\n1. Power off karein\\n2. Pipe connection check karein\\n3. Call technician: +91-99999-12345")
    elif "warranty" in incoming_msg or "af2023x1001" in incoming_msg:
        msg.body("✅ Serial No: AF2023X1001\\n📅 Purchase Date: 15-Jun-2023\\n🛡️ Warranty Valid Till: 15-Jun-2026")
    elif "technician" in incoming_msg:
        msg.body("📞 Technician: +91-99999-12345\\n⏰ Timing: 10am – 6pm (Mon–Sat)")
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Alkafresh SmartCare WhatsApp support assistant. Reply in Hinglish."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            reply = response['choices'][0]['message']['content']
            msg.body(reply)
        except Exception as e:
            msg.body("⚠️ Error: Unable to process request. Please try again later.")

    return str(resp)

if __name__ == "__main__":
    # Ensure Flask app runs on the correct port
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
