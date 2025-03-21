from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# --- Routes utilisant la clé fixe (ancienne méthode) ---
key = b'9QsgaRHRrtV2PF9hcJTwjjRZdTEqUtahTImaeudRaZw='
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    token = f.encrypt(valeur.encode())
    return f"Valeur encryptée (clé fixe) : {token.decode()}"

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_decryptee = f.decrypt(token.encode())
        return f"Valeur décryptée (clé fixe) : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage (clé fixe) : {str(e)}", 400

# --- Nouvelles routes avec clé personnelle ---
@app.route('/encrypt_personnel/<path:cle>/<string:valeur>')
def encryptage_personnel(cle, valeur):
    try:
        f_personnel = Fernet(cle.encode())
        token = f_personnel.encrypt(valeur.encode())
        return f"Valeur encryptée (clé personnelle) : {token.decode()}"
    except Exception as e:
        return f"Erreur lors de l'encryptage avec clé personnelle : {str(e)}", 400

@app.route('/decrypt_personnel/<path:cle>/<string:token>')
def decryptage_personnel(cle, token):
    try:
        f_personnel = Fernet(cle.encode())
        valeur_decryptee = f_personnel.decrypt(token.encode())
        return f"Valeur décryptée (clé personnelle) : {valeur_decryptee.decode()}"
    except InvalidToken:
        return "Erreur : le token n'est pas valide ou la clé est incorrecte.", 400
    except Exception as e:
        return f"Erreur lors du décryptage avec clé personnelle : {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True)
