from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

key = b'9QsgaRHRrtV2PF9hcJTwjjRZdTEqUtahTImaeudRaZw='
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    token = f.encrypt(valeur.encode())
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_decryptee = f.decrypt(token.encode())
        return f"Valeur décryptée : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True)
