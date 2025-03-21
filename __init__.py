from cryptography.fernet import Fernet, InvalidToken
from flask import Flask

app = Flask(__name__)

# ============================
# =  CLÉ FIXE (Ancienne)     =
# ============================
CLE_FIXE = b'9QsgaRHRrtV2PF9hcJTwjjRZdTEqUtahTImaeudRaZw='  # Ta clé fixe
f = Fernet(CLE_FIXE)

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

# ==========================================
# =  CLÉ PERSONNELLE (Nouvelles routes)    =
# ==========================================
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

# =============================
# =  PAGE D'ACCUEIL (HTML/JS)  =
# =============================
@app.route('/')
def home():
    # On renvoie directement le HTML + CSS + JS
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>CryptoPython - Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            max-width: 700px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 5px 0 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button[type="submit"] {
            background-color: #5cb85c;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            background-color: #4cae4c;
        }
        .result {
            margin: 10px 0;
            padding: 10px;
            background: #eee;
            border-radius: 4px;
        }
        hr {
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CryptoPython - Interface</h1>

        <!-- 1) Encrypt (Clé fixe) -->
        <h2>1) Encrypt (Clé fixe)</h2>
        <form id="fixedEncryptForm">
            <label for="fixedEncryptText">Texte à chiffrer :</label>
            <input type="text" id="fixedEncryptText" required>
            <button type="submit">Chiffrer (Clé fixe)</button>
        </form>
        <div id="fixedEncryptResult" class="result"></div>

        <!-- 2) Decrypt (Clé fixe) -->
        <h2>2) Decrypt (Clé fixe)</h2>
        <form id="fixedDecryptForm">
            <label for="fixedDecryptToken">Token à déchiffrer :</label>
            <input type="text" id="fixedDecryptToken" required>
            <button type="submit">Déchiffrer (Clé fixe)</button>
        </form>
        <div id="fixedDecryptResult" class="result"></div>

        <hr>

        <!-- 3) Encrypt (Clé personnelle) -->
        <h2>3) Encrypt (Clé personnelle)</h2>
        <form id="personalEncryptForm">
            <label for="personalKeyEncrypt">Clé (base64) :</label>
            <input type="text" id="personalKeyEncrypt" required>
            <label for="personalTextEncrypt">Texte à chiffrer :</label>
            <input type="text" id="personalTextEncrypt" required>
            <button type="submit">Chiffrer (Clé perso)</button>
        </form>
        <div id="personalEncryptResult" class="result"></div>

        <!-- 4) Decrypt (Clé personnelle) -->
        <h2>4) Decrypt (Clé personnelle)</h2>
        <form id="personalDecryptForm">
            <label for="personalKeyDecrypt">Clé (base64) :</label>
            <input type="text" id="personalKeyDecrypt" required>
            <label for="personalTokenDecrypt">Token à déchiffrer :</label>
            <input type="text" id="personalTokenDecrypt" required>
            <button type="submit">Déchiffrer (Clé perso)</button>
        </form>
        <div id="personalDecryptResult" class="result"></div>
    </div>

    <script>
    // ========== 1) Encrypt (Clé fixe) ==========
    document.getElementById('fixedEncryptForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const text = encodeURIComponent(document.getElementById('fixedEncryptText').value);

        fetch('/encrypt/' + text)
            .then(res => res.text())
            .then(data => {
                document.getElementById('fixedEncryptResult').textContent = data;
            })
            .catch(err => {
                document.getElementById('fixedEncryptResult').textContent = 'Erreur : ' + err;
            });
    });

    // ========== 2) Decrypt (Clé fixe) ==========
    document.getElementById('fixedDecryptForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const token = encodeURIComponent(document.getElementById('fixedDecryptToken').value);

        fetch('/decrypt/' + token)
            .then(res => res.text())
            .then(data => {
                document.getElementById('fixedDecryptResult').textContent = data;
            })
            .catch(err => {
                document.getElementById('fixedDecryptResult').textContent = 'Erreur : ' + err;
            });
    });

    // ========== 3) Encrypt (Clé personnelle) ==========
    document.getElementById('personalEncryptForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const key = encodeURIComponent(document.getElementById('personalKeyEncrypt').value);
        const text = encodeURIComponent(document.getElementById('personalTextEncrypt').value);

        fetch('/encrypt_personnel/' + key + '/' + text)
            .then(res => res.text())
            .then(data => {
                document.getElementById('personalEncryptResult').textContent = data;
            })
            .catch(err => {
                document.getElementById('personalEncryptResult').textContent = 'Erreur : ' + err;
            });
    });

    // ========== 4) Decrypt (Clé personnelle) ==========
    document.getElementById('personalDecryptForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const key = encodeURIComponent(document.getElementById('personalKeyDecrypt').value);
        const token = encodeURIComponent(document.getElementById('personalTokenDecrypt').value);

        fetch('/decrypt_personnel/' + key + '/' + token)
            .then(res => res.text())
            .then(data => {
                document.getElementById('personalDecryptResult').textContent = data;
            })
            .catch(err => {
                document.getElementById('personalDecryptResult').textContent = 'Erreur : ' + err;
            });
    });
    </script>
</body>
</html>
    """

# ============ Lancement local ============
if __name__ == "__main__":
    app.run(debug=True)
