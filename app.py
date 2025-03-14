import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Token xác minh webhook & Token truy cập trang
VERIFY_TOKEN = "02_08_2005"
PAGE_ACCESS_TOKEN = "EAAS4jSnR7ZBcBOwVTMrGqRdE3qkHuMNdYoFfESxdaqyxGkULRdrcSULNGY67ZCY49SV6I9edhyFMhmoLq8TMweHdMhDRJB480VguU6YjZASrZCsC4Qh52n5ytTyZAWj0TKM6ykVa5KGwiTm9oAFLXJyZCml7cZB4PDzyZADT7op1EHMPOh5Ha8quN7Jecfp8b7Jf"

# Route cho trang chủ (để kiểm tra server)
@app.route('/')
def home():
    return "Hello! Flask app is running."

# Route xác minh webhook với Facebook
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification token mismatch", 403

# Route nhận tin nhắn từ Facebook Messenger
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    send_message(sender_id, f"Bạn đã nhắn: {message_text}")
    return "ok", 200

# Hàm gửi tin nhắn
def send_message(recipient_id, message_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post("https://graph.facebook.com/v19.0/me/messages", json=payload, headers=headers)
    if response.status_code != 200:
        print("Lỗi khi gửi tin nhắn:", response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

