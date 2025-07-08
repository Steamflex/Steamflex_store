from flask import Flask, request, redirect, jsonify
import json
import os

app = Flask(__name__)

COMMANDES_FILE = 'commandes.json'

# Fonction pour lire les commandes existantes
def load_commandes():
    if not os.path.exists(COMMANDES_FILE):
        return []
    with open(COMMANDES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

# Fonction pour sauvegarder commandes
def save_commandes(data):
    with open(COMMANDES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/commande', methods=['POST'])
def recevoir_commande():
    data = request.form
    jeux = data.get('Jeux_demandes', '').strip()
    email = data.get('Email_client', '').strip()
    whatsapp = data.get('Whatsapp', '').strip()
    message = data.get('Message_client', '').strip()

    if not jeux or not email:
        return "Erreur : Jeux et email obligatoires.", 400

    commandes = load_commandes()

    nouvelle_commande = {
        "jeux": jeux,
        "email": email,
        "whatsapp": whatsapp,
        "message": message,
        "statut": "Attente"
    }

    commandes.append(nouvelle_commande)
    save_commandes(commandes)

    # Redirige vers page merci locale (à toi de créer merci.html)
    return redirect('/merci.html')

@app.route('/commandes', methods=['GET'])
def get_commandes():
    commandes = load_commandes()
    return jsonify(commandes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
