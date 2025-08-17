from flask import request, jsonify
import bcrypt
from servizi.servizioAutenticatore import crea_token
from servizi.servizioDB import connetti_db

def login():
    """
    Gestisce il processo di login utente.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        # Usa il servizio per verificare le credenziali
        conn = connetti_db()
        cur = conn.cursor()
    
        # Recupera l'utente dal database
        cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s;", (username,))
        user_data = cur.fetchone()
    
        cur.close()
        conn.close()
    
        if user_data:
            user_id, user_name, password_hash = user_data
            # Confronta la password inserita con l'hash salvato
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                user = {
                    'id': user_id,
                    'username': user_name
                }
                
        if user:
            # Crea un token JWT e lo restituisce al client
            token = crea_token(user['id'])
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user_id': user['id']
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def register():
    print("Attempting to register user")
    return 200

