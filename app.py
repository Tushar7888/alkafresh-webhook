from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "demo x1" in incoming_msg:
        msg.body("📽️ Alkafresh X1 Demo Video: https://youtu.be/demo_x1")
    elif "error e3" in incoming_msg:
        msg.body("🛠️ Error E3 - Water Flow Sensor Problem:\n1. Power off karein\n2. Pipe check karein\n3. Technician ko call karein")
    elif "warranty" in incoming_msg:
        msg.body("✅ Serial No: AF2023X1001\n📅 Purchase Date: 15-Jun-2023\n🔒 Warranty Till: 15-Jun-2026")
    else:
        msg.body("❓ Sorry, mujhe samajh nahi aaya. Type 'demo x1', 'error e3', or 'warranty' for help.")

    return str(resp)

if __name__ == "__main__":
    app.run()
