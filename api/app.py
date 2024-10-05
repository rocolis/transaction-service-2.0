import os
import re
import json
import random
import string
import hashlib
import datetime
import requests
import jwt
import paypalrestsdk
from flask import Flask, request, jsonify, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId
from functools import wraps
from flask_cors import CORS
from flask_compress import Compress
from dotenv import load_dotenv
from utils import return_sub_using_email

# Load environment variables
load_dotenv()

# Initialize Flask app and configure extensions
app = Flask(__name__)
CORS(app)
Compress(app)

# MongoDB configuration
MONGOURI = os.environ.get("MONGOURI")
DBNAME = os.environ.get("DBNAME")
USERSCOLLECTIONNAME = os.environ.get("USERSCOLLECTIONNAME")
CLIENT = MongoClient(MONGOURI)
db = CLIENT[DBNAME]
users_collection = db[USERSCOLLECTIONNAME]

# Payment-related configurations
SECRET_KEY = os.environ.get("SECRET")
API_KEY_PAYTECH = os.environ.get("API_PAYTECH")
API_SECRET = os.environ.get("API_SECRET")
payment_request_url = "https://paytech.sn/api/payment/request-payment"
ORANGE_MONEY_API_URL = os.environ.get("ORANGE_MONEY_API_URL")
ORANGE_MONEY_API_KEY = os.environ.get("ORANGE_MONEY_API_KEY")
ORANGE_MONEY_SECRET_KEY = os.environ.get("ORANGE_MONEY_SECRET_KEY")

# Email validation regex
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# PayPal SDK configuration (sandbox mode)
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.environ.get("PAYPAL_CLIENT_ID"),
    "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET")
})


# Token authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            token = token.split(" ")[1]
            sub = kwargs.get('sub') or extract_sub_from_data(request.get_json())

            if sub and re.fullmatch(regex, sub):
                sub = return_sub_using_email(sub, users_collection)

            if not sub:
                return jsonify({'message': 'Sub is missing or invalid'}), 400

            current_user = users_collection.find_one({'_id': ObjectId(sub)})
            if not current_user:
                return jsonify({'message': 'User not found'}), 404

            jwt.decode(token, current_user['secret_key'], algorithms=['HS256'])
            current_user['_id'] = str(current_user['_id'])

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 500

        kwargs['current_user'] = current_user
        return f(*args, **kwargs)

    return decorated


def extract_sub_from_data(data):
    if isinstance(data, list):
        for obj in data:
            if isinstance(obj, dict) and 'sub' in obj:
                return obj.get('sub')
    if isinstance(data, dict):
        return data.get('sub')
    return None


def generate_reference(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def hash_token(token, salt):
    return hashlib.sha256((token + salt).encode()).hexdigest()


# Payment routes
@app.route('/create-payment', methods=['POST'])
def create_paypal_payment():
    amount = request.form['amount']

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{"amount": {"total": amount, "currency": "USD"}, "description": "Example order"}],
        "redirect_urls": {
            "return_url": url_for('execute_payment', _external=True),
            "cancel_url": url_for('cancel_payment', _external=True)
        }
    })

    if payment.create():
        approval_url = payment['links'][1]['href']
        return redirect(approval_url)
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


# Orange Money payment routes
@app.route('/create-payment', methods=['POST'])
def create_orange_money_payment():
    amount = request.form.get('amount')

    data = {
        "amount": amount,
        "currency": "XOF",
        "order_id": generate_reference(),
        "return_url": url_for('execute_payment_', _external=True),
        "cancel_url": url_for('cancel_payment_', _external=True)
    }

    headers = {
        'Authorization': f'Bearer {ORANGE_MONEY_API_KEY}',
        'Content-Type': 'application/json',
        'Secret-Key': ORANGE_MONEY_SECRET_KEY
    }

    response = requests.post(f"{ORANGE_MONEY_API_URL}/create-payment", json=data, headers=headers)

    if response.status_code == 200:
        payment_url = response.json().get('payment_url')
        return jsonify({'payment_url': payment_url})
    else:
        return jsonify({'error': response.json()}), response.status_code


@app.route('/payment/execute', methods=['GET'])
def execute_payment_():
    payment_id = request.args.get('paymentId')

    headers = {
        'Authorization': f'Bearer {ORANGE_MONEY_API_KEY}',
        'Content-Type': 'application/json',
        'Secret-Key': ORANGE_MONEY_SECRET_KEY
    }

    response = requests.get(f"{ORANGE_MONEY_API_URL}/validate-payment/{payment_id}", headers=headers)

    if response.status_code == 200:
        return jsonify({'status': 'Payment executed successfully!'})
    else:
        return jsonify({'error': response.json()}), response.status_code


@app.route('/payment/cancel', methods=['GET'])
def cancel_payment_():
    return jsonify({'status': 'Payment canceled!'})


# Business/Pro payment route
@app.route('/api/v1/payement/pro', methods=['POST'])
@token_required
def payement_rocolis_pro(current_user):
    token = generate_reference()
    data = request.get_json()
    user_id = data.get("sub")

    crypted_token = hash_token(token, "120")
    fake_crypted_token = hash_token(generate_reference(10), "120")

    params_pro = {
        "item_name": "Rocolis abonnement professionnel",
        "item_price": "200",
        "currency": "XOF",
        "ref_command": token,
        "command_name": "Paiement abonnement pro",
        "env": "test",
        "ipn_url": "https://rocolis-payement-service.onrender.com/ipn",
        "success_url": f"https://rocolis-xxx--five.vercel.app/payement/{fake_crypted_token}/{fake_crypted_token}/{crypted_token}/{fake_crypted_token}",
        "cancel_url": "https://domaine.com/cancel",
        "custom_field": json.dumps({"type_abonnement": "pro", "custom_field2": "N/A"})
    }

    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user and user.get("account_type") in ["business", "pro"]:
        return jsonify({"message": "Subscription already active"}), 401

    response = requests.post(payment_request_url, json=params_pro, headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "API_KEY": API_KEY_PAYTECH,
        "API_SECRET": API_SECRET
    })

    if response.status_code == 200:
        users_collection.update_one({"_id": ObjectId(user_id)},
                                    {"$set": {"payement_token": token, "status_token": crypted_token}})
        return response.json()
    else:
        return jsonify({"message": "Payment processing error."}), response.status_code


if __name__ == '__main__':
    from waitress import serve

    serve(app)
