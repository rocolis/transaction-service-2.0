import datetime
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

API_KEY_PAYTECH = os.environ.get("API_PAYTECH")
API_SECRET = os.environ.get("API_SECRET")

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


@app.route('/api/v1/payement/pro', methods=['POST'])
@token_required
def payement_rocolis_pro(current_user):
    token = generate_reference()
    data = request.get_json()
    user_id = data.get("sub")

    def hash_token(tokens, salt):
        return hashlib.sha256((tokens + salt).encode()).hexdigest()

    crypted_token = hash_token(token, "120")
    fake_crypted_token = hash_token(generate_reference(10), "120")

    params_pro = {
        "item_name": "Rocolis abonnement professionnel",
        "item_price": "200",  # Mettez à jour le prix si nécessaire
        "currency": "XOF",
        "ref_command": token,
        "command_name": "Paiement abonnement pro",
        "env": "test",
        "ipn_url": "https://rocolis-payement-service.onrender.com/ipn",
        "success_url": f"https://rocolis-xxx--five.vercel.app/payement/{fake_crypted_token}/{fake_crypted_token}/{crypted_token}/{fake_crypted_token}",
        "cancel_url": "https://domaine.com/cancel",
        "custom_field": json.dumps({
            "type_abonnement": "pro",
            "custom_field2": "N/A",
        })
    }

    # Vérifier si l'utilisateur a déjà un abonnement actif
    if users_collection.find_one({"_id": ObjectId(user_id)}).get("account_type") in ["business", "pro"]:
        return jsonify({"message": "Vous avez déjà un abonnement en cours, veuillez attendre la fin de celui-ci pour "
                                   "changer ou continuer votre plan."}), 401

    response = requests.post(payment_request_url, json=params_pro, headers=headers)

    if response.status_code == 200:
        # Mettre à jour le champ `payement_token` dans la base de données
        users_collection.update_one({"_id": ObjectId(user_id)},
                                    {"$set": {"payement_token": token, "status_token": crypted_token}})
        json_response = response.json()
        return json_response
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return jsonify({"message": "Erreur lors du traitement du paiement."}), response.status_code


@app.route('/ipn', methods=['POST'])
def ipn_listener():
    ipn_data = request.form.to_dict()
    print(ipn_data)
    process_ipn(ipn_data)
    return "IPN reçu", 200


@app.route('/', methods=['GET'])
def index():
    return "running running", 200


import json


def process_ipn(ipn_data):
    ref_command = ipn_data.get('ref_command')
    payment_method = ipn_data.get('payment_method')
    amount_paid = ipn_data.get('item_price')
    payment_status = ipn_data.get('type_event')

    # Désérialiser le champ 'custom_field'
    try:
        type_abonnement_main = json.loads(ipn_data.get("custom_field", "{}"))
    except json.JSONDecodeError:
        print(f"Erreur lors de la désérialisation de 'custom_field' pour la commande {ref_command}")
        return

    type_abonnement = type_abonnement_main.get("type_abonnement")
    user = users_collection.find_one({"payement_token": ref_command})

    if user:
        if payment_status == "sale_complete":
            print(f"Paiement réussi pour la commande : {ref_command}")
            update_fields = {}
            if type_abonnement == "business":
                update_fields = {
                    "account_type": "business",
                    "max_weight": 50,
                    "started_abonnement": datetime.datetime.utcnow()
                }
            elif type_abonnement == "pro":
                update_fields = {
                    "account_type": "pro",
                    "max_weight": 100,
                    "started_abonnement": datetime.datetime.utcnow(),
                    "payment_method": payment_method
                }
            users_collection.update_one({"payement_token": ref_command}, {"$set": update_fields})
            print(f"Utilisateur {user['_id']} mis à jour avec succès.")
            users_collection.update_one({"payement_token": ref_command}, {"$unset": {"payement_token": ""}})
            print(f"Le champ 'payement_token' pour l'utilisateur {user['_id']} a été supprimé.")
        else:
            print(f"Statut de paiement : {payment_status}, aucun changement effectué.")
    else:
        print(f"Commande avec la référence {ref_command} non trouvée dans la base de données.")


@app.route('/api/v1/check/payement/status', methods=['POST'])
def check_payement_status():
    data = request.get_json()
    status_token = data.get("status_token")

    user = users_collection.find_one({"status_token": status_token})
    if user:
        user_type = user.get("account_type")
        users_collection.delete_one({"status_token": status_token})

        return jsonify({"message": "success", "userType": user_type}), 200
    else:
        return jsonify({"error": "error"}), 404


@app.route('/api/v1/payement/business', methods=['POST'])
@token_required
def payement_rocolis_business(current_user):
    try:
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
            "ipn_url": "https://rocolis-payement-service.onrender.com/ipn",
            "success_url": f"https://rocolis-xxx--five.vercel.app/payement/{fake_crypted_token}/{fake_crypted_token}/{crypted_token}/{fake_crypted_token}",
            "cancel_url": "https://domaine.com/cancel",
            "custom_field": json.dumps({
                "type_abonnement": "business",
                "custom_field2": "N/A",
            })
        }

        print("je suis icic")
        if users_collection.find_one({"_id": ObjectId(user_id)}).get("account_type") in ["business", "pro"]:
            return jsonify({"message": "Vous avez déjà abonnement encours, veuillez attendre la fin de celui ci pour "
                                       "changer ou continuer votre plan"}), 401

        response = requests.post(payment_request_url, json=params_business, headers=headers)

        if response.status_code == 200:
            collection = users_collection.find_one({"_id": ObjectId(user_id)})
            if collection:
                users_collection.update_one({"_id": ObjectId(user_id)},
                                            {"$set": {"payement_token": token, "status_token": crypted_token}})
            json_response = response.json()
            return json_response
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    from waitress import serve
    serve(app)
