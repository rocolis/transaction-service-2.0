import os

import paypalrestsdk
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for

load_dotenv()

app = Flask(__name__)

"""#####################################-PayPal-###########################################"""
# Configuration PayPal en mode sandbox
paypalrestsdk.configure({
    "mode": "sandbox",  # Utiliser "live" pour le mode production
    "client_id": os.environ.get("PAYPAL_CLIENT_ID"),  # Remplacer par votre client ID PayPal sandbox
    "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET")  # Remplacer par votre secret client PayPal sandbox
})

# Page pour entrer le montant de la commande
@app.route('/')
def index():
    return render_template('index.html')

# Route pour créer une transaction de paiement avec le montant saisi par l'utilisateur
@app.route('/create-payment', methods=['POST'])
def create_payment():
    amount = request.form['amount']  # Montant de la commande

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": amount,  # Utiliser le montant saisi
                "currency": "USD"},
            "description": "Commande d'exemple"}],
        "redirect_urls": {
            "return_url": url_for('execute_payment', _external=True),  # URL de retour après succès
            "cancel_url": url_for('cancel_payment', _external=True)  # URL d'annulation
        }
    })

    if payment.create():
        approval_url = payment['links'][1]['href']  # Lien pour approuver le paiement
        return redirect(approval_url)  # Rediriger l'utilisateur vers PayPal pour le paiement
    else:
        return jsonify({'error': payment.error}), 500

# Route pour exécuter le paiement après approbation PayPal
@app.route('/payment/execute')
def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return jsonify({'status': 'Payment executed successfully!'})
    else:
        return jsonify({'error': payment.error}), 500

# Route en cas d'annulation de paiement
@app.route('/payment/cancel')
def cancel_payment():
    return jsonify({'status': 'Payment canceled!'})

"""#####################################-PayPal_End-###########################################"""

"""#####################################-Orange-###########################################
# Charger les informations d'API
ORANGE_MONEY_API_URL = os.environ.get("ORANGE_MONEY_API_URL")
ORANGE_MONEY_API_KEY = os.environ.get("ORANGE_MONEY_API_KEY")
ORANGE_MONEY_SECRET_KEY = os.environ.get("ORANGE_MONEY_SECRET_KEY")

@app.route('/create-payment', methods=['POST'])
def create_payment():
    amount = request.form.get('amount')

    # Préparer les données pour Orange Money
    data = {
        "amount": amount,
        "currency": "XOF",  # ou la devise utilisée par Orange Money
        "order_id": "unique_order_id_here",
        "return_url": "http://localhost:5000/payment/execute",
        "cancel_url": "http://localhost:5000/payment/cancel"
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
def execute_payment():
    payment_id = request.args.get('paymentId')

    # Valider le paiement auprès de l'API d'Orange Money
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
def cancel_payment():
    return jsonify({'status': 'Payment canceled!'})"""

if __name__ == '__main__':
    app.run(debug=True)
