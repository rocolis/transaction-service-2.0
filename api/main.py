from flask import Flask, request, jsonify
import paypalrestsdk
import os
from dotenv import load_dotenv
from flask_compress import Compress
from flask_cors import CORS
from pymongo import MongoClient

load_dotenv()

SECRET_KEY = os.environ.get("SECRET")
MONGOURI = os.environ.get("MONGOURI")
DBNAME = os.environ.get("DBNAME")
USERSCOLLECTIONNAME = os.environ.get("USERSCOLLECTIONNAME")

CLIENT = MongoClient(MONGOURI)
db = CLIENT[DBNAME]
users_collection = db[USERSCOLLECTIONNAME]

app = Flask(__name__)
CORS(app)
Compress(app)
app.config['SECRET_KEY'] = SECRET_KEY

# Configuration PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Utiliser "live" pour le mode production
    "client_id": os.environ.get("AUAnBMM6yCy3e3mEhM6NB8-uBcUcufuWsm--PvmFzcbYjmnKuRFpoJzmtoMWHslXyNzCEJghCAam98iq"),
    "client_secret": os.environ.get("EHG6b87oub44aq61dLvhZORQx4_wY1knINwntqJp7Q1M4vx8WdjHm9tScIkzYMv7JvalzdQZAXSpYR3P")
})

@app.route('/create-payment', methods=['POST'])
def create_payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": "10.00", "currency": "USD"},
            "description": "Transaction example"
        }],
        "redirect_urls": {
            "return_url": "https://rocolis.vercel.app/payment/execute",
            "cancel_url": "https://rocolis.vercel.app/payment/cancel"
        }
    })

    if payment.create():
        return jsonify({'paymentID': payment.id})
    else:
        return jsonify({'error': payment.error}), 500

@app.route('/payment/execute', methods=['GET'])
def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return jsonify({'status': 'Payment executed successfully!'})
    else:
        return jsonify({'error': payment.error}), 500

@app.route('/payment/cancel', methods=['GET'])
def cancel_payment():
    return jsonify({'status': 'Payment canceled!'})

if __name__ == '__main__':
    app.run(debug=True)
