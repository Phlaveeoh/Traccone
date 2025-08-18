from flask import request, jsonify
from functools import wraps
import bcrypt
import jwt
import os

def hash_password(password):
    """
    Genera un hash bcrypt valido per una password.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def crea_token(user_id):
    """
    Crea un token JWT per l'utente.
    """
    payload = {'user_id': user_id}
    return jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')

def valida_token(f):
    """
    Verifica la presenza e la validità del token nell'intestazione Authorization.
    Se il token è valido, passa l'ID utente alla funzione decorata.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Ottiene il token dall'intestazione della richiesta
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Il token è nel formato "Bearer <token>", quindi lo estraiamo
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"errore": "Formato dell'intestazione non valido. Usare Bearer <token>"}), 401

        if not token:
            return jsonify({"errore": "Token di autenticazione mancante!"}), 401

        try:
            # Decodifica il token con la chiave segreta
            payload = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])
            current_user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return jsonify({"errore": "Token scaduto, effettuare di nuovo il login"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"errore": "Token non valido"}), 401
        
        # Passa l'ID utente alla funzione decorata
        return f(current_user_id, *args, **kwargs)

    return decorated