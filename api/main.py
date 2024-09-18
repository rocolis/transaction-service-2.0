from flask import Flask, request, jsonify
import paypalrestsdk
import os
from dotenv import load_dotenv
from flask_compress import Compress
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
Compress(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET')

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.environ.get("PAYPAL_CLIENT_ID"),
    "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET")
})

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": "10.00", "currency": "USD"},
            "description": "Transaction example"
        }],
        "redirect_urls": {
            "return_url": "https://transaction-service-2-0.vercel.app/api/payment/execute",
            "cancel_url": "https://transaction-service-2-0.vercel.app/api/payment/cancel"
        }
    })

    if payment.create():
        return jsonify({'paymentID': payment.id})
    else:
        return jsonify({'error': payment.error}), 500

@app.route('/api/payment/execute', methods=['GET'])
def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return jsonify({'status': 'Payment executed successfully!'})
    else:
        return jsonify({'error': payment.error}), 500

@app.route('/api/payment/cancel', methods=['GET'])
def cancel_payment():
    return jsonify({'status': 'Payment canceled!'})

if __name__ == '__main__':
    app.run(debug=True)
