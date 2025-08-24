from flask import request, jsonify
import traceback
from servizi.servizioDB import connetti_db

def updateUtente(userID):
    # TODO : update; tuttoh
    # 
    pass

def eliminaUtente(userID):
    # TODO : update; tuttoh
    # 
    pass

def prendiUtente(user_id):
    try :
        conn = connetti_db()
        cur = conn.cursor()

        cur.execute("SELECT username, telefono, nome, cognome from users where id = %s", (user_id,))
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
   