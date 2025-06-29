from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Webhook triggered!")  # Render logs me dikhega
    incoming_msg = request.form.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "demo" in incoming_msg:
        msg.body("📹 Demo X1 Video: https://youtu.be/demo_x1")
    else:
        msg.body("✅ Flask is live. Type 'demo' for video link.")
    
    return str(resp)
