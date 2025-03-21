from cryptography.fernet import Fernet, InvalidToken
from flask import Flask

app = Flask(__name__)

# =========================
# =  PAGE D'ACCUEIL (HTML) =
# =========================
@app.route('/')
def home():
    # On renvoie le HTML directement depuis le code Python
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
            max-width: 600px;
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
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 5px 0 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #5cb85c;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #4cae4c;
        }
        .note {
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CryptoPython - Interface</h1>

        <h2>1) Encryption (Clé fixe)</h2>
        <p>
            Pour tester rapidement l'encryptage avec la clé fixe, rendez-vous sur :
            <br>
            <code>/encrypt/TON_TEXTE</code>
        </p>

        <h2>2) Décryption (Clé fixe)</h2>
        <p>
            Pour tester rapidement le décryptage avec la clé fixe, rendez-vous sur :
            <br>
            <code>/decrypt/TON_TOKEN</code>
        </p>

        <hr>

        <h2>3) Encryption (Clé personnelle)</h2>
        <form id="encryptForm">
            <label for="encryptKey">Clé (base64) :</label>
            <input type="text" id="encryptKey" name="encryptKey" placeholder="Ex: I8hopNtR9Wkt0lzeiZjPf_GaDB-..." required>
            <label for="plainText">Texte à chiffrer :</label>
            <input type="text" id="plainText" name="plainText" placeholder="bonjour" required>
            <input type="submit" value="Chiffrer">
        </form>

        <h2>4) Décryption (Clé personnelle)</h2>
        <form id="decryptForm">
            <label for="decryptKey">Clé (base64) :</label>
            <input type="text" id="decryptKey" name="decryptKey" placeholder="Ex: I8hopNtR9Wkt0lzeiZjPf_GaDB-..." required>
            <label for="cipherText">Token à déchiffrer :</label>
            <input type="text" id="cipherText" name="cipherText" placeholder="Copie le token généré" required>
            <input type="submit" value="Déchiffrer">
        </form>

        <div class="note">
            <strong>Note :</strong> Pour l'encryptage/décryptage avec clé personnelle, tu seras redirigé vers les URLs :
            <br><code>/encrypt_personnel/LA_CLE/LE_TEXTE</code> et <code>/decrypt_personnel/LA_CLE/LE_TOKEN</code>.
        </div>
    </div>

    <script>
        // Formulaire d'encryptage (clé perso)
        document.getElementById("encryptForm").addEventListener("submit", function(e) {
            e.preventDefault();
            const key = encodeURIComponent(document.getElementById("encryptKey").value);
            const text = encodeURIComponent(document.getElementById("plainText").value);
            window.location.href = "/encrypt_personnel/" + key + "/" + text;
        });

        // Formulaire de décryptage (clé perso)
        document.getElementById("decryptForm").addEventListener("submit", function(e) {
            e.preventDefault();
            const key = encodeURIComponent(document.getElementById("decryptKey").value);
            const token = encodeURIComponent(document.getElementById("cipherText").value);
            window.location.href = "/decrypt_personnel/" + key + "/" + token;
        });
    </script>
</body>
</html>
    """

# ===========================
# =  CLÉ FIXE (Ancienne)    =
# ===========================
key = b'9QsgaRHRrtV2PF9hcJTwjjRZdTEqUtahTImaeudRaZw='  # Ta clé fixe
f = Fernet(key)

# --- Encryption clé fixe ---
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    token = f.encrypt(valeur.encode())
    return f"Valeur encryptée (clé fixe) : {token.decode()}"

# --- Décryption clé fixe ---
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_decryptee = f.decrypt(token.encode())
        return f"Valeur décryptée (clé fixe) : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage (clé fixe) : {str(e)}", 400

# =====================================
# =  CLÉ PERSONNELLE (Nouvelles routes)
# =====================================
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

# =========================
# =   Lancement (dev)     =
# =========================
if __name__ == "__main__":
    app.run(debug=True)
