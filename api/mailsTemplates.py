from datetime import datetime

months_translation = {
    "January": "janvier",
    "February": "février",
    "March": "mars",
    "April": "avril",
    "May": "mai",
    "June": "juin",
    "July": "juillet",
    "August": "août",
    "September": "septembre",
    "October": "octobre",
    "November": "novembre",
    "December": "décembre",
}


def evaluation_mail(departureCity, arrivalCity, departureDate, link):
    formatted_date = departureDate.strftime("%A %d %B %Y à %H:%M UTC").replace(
        "Monday", "Lundi"
    ).replace(
        "Tuesday", "Mardi"
    ).replace(
        "Wednesday", "Mercredi"
    ).replace(
        "Thursday", "Jeudi"
    ).replace(
        "Friday", "Vendredi"
    ).replace(
        "Saturday", "Samedi"
    ).replace(
        "Sunday", "Dimanche"
    )
    for month_en, month_fr in months_translation.items():
        formatted_date = formatted_date.replace(month_en, month_fr)
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Évaluation de l'expédition</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png" alt="Logo de la compagnie" />
      </div>
      <div class="content">
        <h1>Évaluez votre expédition</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que votre expédition s'est bien déroulée. Nous vous
          invitons à évaluer votre expérience. Voici les détails de votre
          expédition :
        </p>
        <div class="details">
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Date de départ :</strong> {formatted_date}</p>
        </div>
        <a href="{link}" class="btn">Évaluer l'expédition</a>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>
"""


def confirmation_affectation(departureCity, arrivalCity, weight, parcel_type, link):
    return f"""
  <!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Confirmation de l'affectation</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1>Confirmation de l'affectation</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que vous allez bien. Il semble qu'un expéditeur
          essaie de vous attribuer un colis. Veuillez confirmer l'affectation si
          vous reconnaissez ce colis.
        </p>
        <div class="details">
          <p>Détails du colis :</p>
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Type de colis :</strong> {parcel_type}</p>
          <p><strong>Poids :</strong> {weight} kg</p>
        </div>
        <a href="{link}" class="btn">Confirmer l'affectation</a>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>

  """


def refus_affectation(reason, departureCity, arrivalCity, weight, parcel_type):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Refus de l'affectation</title>
       <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 style="color: red;">Refus de l'affectation</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que vous allez bien. Il semble que votre colis a été refusé par le voyageur.
        </p>
        <p>motif : {reason}</p>
        <div class="details">
          <p>Détails du colis :</p>
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Type de colis :</strong> {parcel_type}</p>
          <p><strong>Poids :</strong> {weight} kg</p>
        </div>
        <p>Veuillez contacter le voyageur pour plus d'informations</p>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>

"""


def confirmation_delivered(departureCity, arrivalCity, weight, parcel_type):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Confirmation de livraison</title>
       <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 style="color: green">Colis Livré</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que vous allez bien. Il semble que votre colis ait été
          marqué comme livré. Nous vous prions de vérifier cela et de contacter
          le voyageur en cas de problème éventuel.
        </p>
        <div class="details">
          <p>Détails du colis :</p>
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Type de colis :</strong> {parcel_type}</p>
          <p><strong>Poids :</strong> {weight} kg</p>
        </div>
        <p>Veuillez contacter le voyageur pour plus d'informations</p>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>

"""


def confirmation_not_delivred(departureCity, arrivalCity, weight, parcel_type):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Confirmation de livraison</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 style="color: red">Colis non livré</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que vous allez bien. Il semble que votre colis ait été
          marqué comme étant livré par erreur. Nous vous prions de vérifier cela et de contacter
          le voyageur en cas de problème éventuel.
        </p>
        <div class="details">
          <p>Détails du colis :</p>
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Type de colis :</strong> {parcel_type}</p>
          <p><strong>Poids :</strong> {weight} kg</p>
        </div>
        <p>Veuillez contacter le voyageur pour plus d'informations</p>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>
"""


def confirmation_accepeted_parcel(departureCity, arrivalCity, weight, parcel_type):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Acceptation de l'affectation</title>
       <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 style="color: green;">Acceptation de l'affectation</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que vous allez bien. Il semble que votre colis ait été accepté par le voyageur.
        </p>
        <div class="details">
          <p>Détails du colis :</p>
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Type de colis :</strong> {parcel_type}</p>
          <p><strong>Poids :</strong> {weight} kg</p>
        </div>
        <p>Veuillez contacter le voyageur pour plus d'informations</p>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>

"""


def traveler_affectation_annulation(motif, departureCity, arrivalCity, weight, parcel_type):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Annulation de l'affectation</title>
       <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 style="color: red;">Annulation de l'affectation</h1>
        <p>Bonjour,</p>
        <p>
          Nous espérons que vous allez bien. L'expéditeur vient d'annuler l'affectation de son colis.
        </p>
        <p>Motif de l'annulation : {motif}</p>
        <div class="details">
          <p>Détails du colis :</p>
          <p><strong>Ville de départ :</strong> {departureCity}</p>
          <p><strong>Ville d'arrivée :</strong> {arrivalCity}</p>
          <p><strong>Type de colis :</strong> {parcel_type}</p>
          <p><strong>Poids :</strong> {weight} kg</p>
        </div>
        <p>Veuillez contacter le voyageur pour plus d'informations</p>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
  
</html>

"""


def received_ad(username):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ROCOLIS - Votre annonce est en cours de validation</title>
       <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 style="color: red">Annonce en cours de validation<h1>
        <p>Bonjour {username},</p>
        <p>
          Votre annonce a bien été reçue. Elle sera
          examinée, et vous recevrez un email de
          confirmation dans les 30 minutes.        </p>
        
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>

"""


def reported_ad(reported_by, reported_ad_id, reporting_cause):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ROCOLIS - Alerte de signalement</title>
         <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <h1 >Alerte de signalement<h1>
        <p>Bonjour Sosthène,</p>
        <p>
          Une annonce viens d'être signalé voici l'id : {reported_ad_id}
        </p>
         <p>
         Signalé par : {reported_by} , raison : {reporting_cause}
        </p>
        
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>
"""


def verification_code(username, code):
    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ROCOLIS - Votre annonce est en cours de validation</title>
         <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        margin-top: 100px;
        padding: 0;
      }}
      .container {{
        width: 100%;
        margin-top: 20px;
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .content .details {{
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
      }}
      .content .details p {{
        margin: 0;
        font-size: 14px;
        color: #555;
      }}
      .content .btn {{
        display: block;
        width: fit-content;
        margin: 0 auto;
        padding: 10px 20px;
        background-color: #171046;
        color: #ffffff;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <p>Bonjour {username},</p>
        <p style="text-align: center;">
          Voici votre code validation :  <div align="center">
            <p
              href="https://unlayer.com"
              target="_blank"
              class="v-size-width"
              style="
                box-sizing: border-box;
                display: inline-block;
                font-family: arial, helvetica, sans-serif;
                text-decoration: none;
                -webkit-text-size-adjust: none;
                text-align: center;
                color: #ffffff;
                background-color: #181147;
                border-radius: 1px;
                -webkit-border-radius: 1px;
                -moz-border-radius: 1px;
                width: 55%;
                padding: 15px 0px 15px 0px;
                max-width: 100%;
                overflow-wrap: break-word;
                word-break: break-word;
                word-wrap: break-word;
              "
            >
            {code}
              
            </p>
          </div>
        </p>
        <span
        style="
          font-size: 16px;
          line-height: 28.8px;
        "
        ><br />Ignorez ce message si vous
        avez déjà confirmé votre compte
      </span>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>

"""


def send_notifications_html(username, notifications):
    notification_items = ""

    for notification in notifications:
        departure_city = notification.get("departureCity", "N/A")
        destination_city = notification.get("destinationCity", "N/A")
        departure_date = notification.get("departureDate", "N/A")
        available_kilos = notification.get("availableKilos", "N/A")
        kilos_price = notification.get("kilosPrice", "N/A")
        link = f"https://rocolis-frontend-tsx.vercel.app/ad/details/{str(notification.get('_id'))}"

        if isinstance(departure_date, datetime):
            departure_date = departure_date.strftime('%d-%m-%Y')

        notification_items += f"""
               <li style="margin-bottom: 20px; padding: 10px; border: 1px solid #e5e5e5; border-radius: 8px;">
                 <strong>Ville de départ:</strong> {departure_city}<br>
                 <strong>Ville d'arrivée:</strong> {destination_city}<br>
                 <strong>Date de départ:</strong> {departure_date}<br>
                 <strong>Kilos disponibles:</strong> {available_kilos}<br>
                 <strong>Prix par kilo:</strong> {kilos_price} XAF<br>
                 <a href="{link}" style="color: #171046; text-decoration: none;">Voir l'annonce</a>
               </li>
               """

    return f"""
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ROCOLIS - Vos notifications</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        color: #333;
        padding: 0;
        margin: 0;
      }}
      .container {{
        width: 100%;
        max-width: 600px;
        margin: 20px auto;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }}
      .header {{
        background-color: #10837f;
        color: #ffffff;
        text-align: center;
        padding: 20px;
      }}
      .header img {{
        width: 200px;
        height: auto;
      }}
      .content {{
        padding: 20px;
      }}
      .content h1 {{
        font-size: 24px;
        margin-bottom: 10px;
      }}
      .content p {{
        font-size: 16px;
        line-height: 1.5;
      }}
      .notification-list {{
        list-style: none;
        padding: 0;
      }}
      .notification-list li {{
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
      }}
      .footer {{
        text-align: center;
        padding: 20px;
        background-color: #171046;
        color: #ffffff;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img
          src="https://i.ibb.co/9YsvN3N/Logotype-Officiel-Rocolis-blanc.png"
          alt="Logo de la compagnie"
        />
      </div>
      <div class="content">
        <p>Bonjour {username},</p>
        <p>Voici les annonces disponibles correspondant à vos critères :</p>
        <ul class="notification-list">
          {notification_items}
        </ul>
      </div>
      <div class="footer">
        <p>Cordialement,</p>
        <p>L'équipe Rocolis</p>
      </div>
    </div>
  </body>
</html>
"""

