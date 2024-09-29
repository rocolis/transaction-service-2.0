import hashlib

import requests
import json
import random
import string

from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt
from functools import wraps
from flask_cors import CORS
from flask_compress import Compress
from bson import ObjectId
from dotenv import load_dotenv
import os
import re
from utils import return_sub_using_email

load_dotenv()

app = Flask(__name__)
USERSCOLLECTIONNAME = os.environ.get("USERSCOLLECTIONNAME")
SECRET_KEY = os.environ.get("SECRET")
MONGOURI = os.environ.get("MONGOURI")
DBNAME = os.environ.get("DBNAME")

CLIENT = MongoClient(MONGOURI)
db = CLIENT[DBNAME]
app = Flask(__name__)
CORS(app)
Compress(app)

users_collection = db[USERSCOLLECTIONNAME]

API_KEY_PAYTECH = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API SECRET")

payment_request_url = "https://paytech.sn/api/payment/request-payment"
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            token = token.split(" ")[1]
            sub = kwargs.get('sub')

            if not sub:
                data = request.get_json()

                if type(data) == list:
                    for obj in data:
                        if isinstance(obj, dict) and 'sub' in obj:
                            sub = obj['sub']
                            break
                if type(data) != list:
                    sub = data.get('sub')
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
            print(e)
            return jsonify({'message': str(e)}), 500

        kwargs['current_user'] = current_user
        return f(*args, **kwargs)

    return decorated


def generate_reference(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


params_professionnel = {
    "item_name": "Rocolis abonnement professionnel",
    "item_price": "100",
    "currency": "XOF",
    "ref_command": "IPHONETEST2",
    "command_name": "Paiement abonnement afaire",
    "env": "test",
    "ipn_url": "https://domaine.com/ipn",
    "success_url": "https://domaine.com/success",
    "cancel_url": "https://domaine.com/cancel",
    "custom_field": json.dumps({
        "custom_field1": "value_1",
        "custom_field2": "value_2",
    })
}
params_affaires = {
    "item_name": "Rocolis abonnement affaire",
    "item_price": "100",
    "currency": "XOF",
    "ref_command": "token",
    "command_name": "Paiement abonnement affaire rocolis",
    "env": "test",
    "ipn_url": "https://domaine.com/ipn",
    "success_url": "https://domaine.com/success",
    "cancel_url": "https://domaine.com/cancel",
    "custom_field": json.dumps({
        "custom_field1": "value_1",
        "custom_field2": "value_2",
    })
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "API_KEY": API_KEY_PAYTECH,
    "API_SECRET": API_SECRET,
}


@app.route('/api/v1/payement/affaire', methods=['POST'])
@token_required
def payement_rocolis_affaires():
    data = request.get_json()
    user_id = data.get("sub")
    response = requests.post(payment_request_url, json=params_affaires, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
    else:
        print(f"Error: {response.status_code}, {response.text}")


@app.route('/ipn', methods=['POST'])
def ipn_listener():
    ipn_data = request.form.to_dict()
    print(ipn_data)
    process_ipn(ipn_data)
    return "IPN reçu", 200


@app.route('/', methods=['GET'])
def index():
    return "running running", 200


def process_ipn(ipn_data):
    payment_status = ipn_data.get('payment_status')
    transaction_id = ipn_data.get('txn_id')
    amount_paid = ipn_data.get('mc_gross')
    payer_email = ipn_data.get('payer_email')

    if payment_status == "Completed":
        print(f"Paiement réussi pour la transaction : {transaction_id}")
    else:
        print(f"Statut de paiement : {payment_status}")


@app.route('/api/v1/payement/business', methods=['POST'])
@token_required
def payement_rocolis_business(current_user):
    token = generate_reference()
    data = request.get_json()
    user_id = data.get("sub")

    def hash_token(tokens, salt):
        return hashlib.sha256((tokens + salt).encode()).hexdigest()

    crypted_token = hash_token(token, "120")
    fake_crypted_token = hash_token(generate_reference(10), "120")

    params_business = {
        "item_name": "Rocolis abonnement professionnel",
        "item_price": "100",
        "currency": "XOF",
        "ref_command": token,
        "command_name": "Paiement abonnement business",
        "env": "test",
        "ipn_url": "http://192.168.1.10:5000/ipn",
        "success_url": f"https://localhost:5173/payement/{fake_crypted_token}/{fake_crypted_token}/{crypted_token}/{fake_crypted_token}",
        "cancel_url": "https://domaine.com/cancel",
        "custom_field": json.dumps({
            "custom_field1": "N/A",
            "custom_field2": "N/A",
        })
    }

    response = requests.post(payment_request_url, json=params_business, headers=headers)

    if response.status_code == 200:
        collection = users_collection.find_one({"_id": ObjectId(user_id)})
        if collection:
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"payement_token": token}})
        json_response = response.json()
        print(json_response)
    else:
        print(f"Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
    from waitress import serve
    serve(app)
