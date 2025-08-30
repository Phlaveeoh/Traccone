from flask import request, jsonify
import bcrypt
import traceback
from servizi.servizioAutenticatore import crea_token, hash_password
from servizi.servizioDB import connetti_db

def login():
    """
    Gestisce il processo di login utente.
    """
    #Prende i dati JSON dalla richiesta
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    #Controlla che username e password siano stati forniti altrimenti ritorna un errore
    if not all([username, password]):
        return jsonify({'error': 'Mancano username o password'}), 400

    try:
        #Connessione al database
        conn = connetti_db()
        cur = conn.cursor()
    
        #Recupera l'utente dal database
        cur.execute("SELECT id, username, password FROM users WHERE username = %s;", (username,))
        user_data = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()
    
        #Se l'utente non esiste nel database restituisci un errore
        if not user_data:
            return jsonify({'error': 'Credenziali invalide'}), 401

        user_id, user_name, password_hash = user_data
        
        #Confronta la password inserita con l'hash salvato
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            #Se la password è corretta, crea il token e restituisci la risposta di successo
            token = crea_token(user_id)
            return jsonify({
                'message': 'Login effettuato con successo',
                'token': token,
                'user_id': user_id
            }), 200
        else:
            #Se la password è sbagliata, restituisci un errore
            return jsonify({'error': 'Credenziali invalide'}), 401

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


def register():
    """
    Gestisce il processo di login utente.
    """
    #Prende i dati JSON dalla richiesta
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    #Controlla che username e password siano stati forniti altrimenti ritorna un errore
    if not all([username, password]):
        return jsonify({'error': 'Mancano username o password'}), 400

    try:
        #Connessione al database
        conn = connetti_db()
        cur = conn.cursor()

        #Controlla se l'username esiste già
        cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
        if cur.fetchone():
            return jsonify({'error': 'Username già esistente'}), 409

        #Crea un nuovo utente
        hashed_password = hash_password(password) #Hash della password
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;", (username, hashed_password))
        user_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        #Crea il token per il nuovo utente
        token = crea_token(user_id)
        return jsonify({
            'message': 'Registrazione avvenuta con successo',
            'token': token,
            'user_id': user_id
        }), 201

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500