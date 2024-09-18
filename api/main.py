from flask import Flask, request, jsonify, render_template, redirect, url_for
import paypalrestsdk
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
