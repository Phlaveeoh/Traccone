from flask import request, jsonify
import traceback
import psycopg2.extras
from servizi.servizioDB import connetti_db

def update(userID):
    # TODO : update; tuttoh
    # 
    pass

def eliminaUtente(userID):
    try :
        conn = connetti_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = %s", (userID,))
        response = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if response:
            return jsonify({
                'message': "successo",
            }), 204
        else:
            return jsonify({'message': 'nessun utente trovato'}), 404
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500
    

def prendiUtente(userID):
    try :
        conn = connetti_db()
        cur = conn.cursor()

        cur.execute("SELECT username, telefono, nome, cognome from users where id = %s", (userID,))
        userData = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if userData:
            username = userData[0]
            telefono = userData[1]
            nome = userData[2]
            cognome = userData[3]
            
            return jsonify({
                'username': username,
                'telefono': telefono,
                'nome': nome,
                'cognome': cognome
            }), 200
        else:
            return jsonify({'message': 'nessun utente trovato'}), 404
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500
   