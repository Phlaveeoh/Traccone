from flask import request, jsonify
import traceback
import bcrypt
from servizi.servizioDB import connetti_db
from servizi.servizioAutenticatore import hash_password

#Metodo per aggiornare un utente
def updateUtente(userID):
    data = request.get_json()
    telefono = data.get('telefono')
    nome = data.get('nome')
    cognome = data.get('cognome')

    try :
        conn = connetti_db()
        cur = conn.cursor()

        cur.execute("UPDATE users SET telefono = %s,nome = %s,cognome = %s WHERE id = %s RETURNING id", (telefono, nome, cognome, userID,))
        aggiornato = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if aggiornato:
            return jsonify({
                "message": "Utente aggiornato con successo"
            }), 200
        else:
            return jsonify({'message': 'nessun utente trovato'}), 404
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

#Metodo per cambiare la password
def cambiaPassword(user_id):
    data = request.get_json()
    vecchia_password = data.get('vecchia_password')
    nuova_password = data.get('nuova_password')

    try :
        conn = connetti_db()
        cur = conn.cursor()
        
        # Recupero la password attuale
        cur.execute("SELECT password from users where id = %s", (user_id,))
        password_attuale = cur.fetchone()
        #Controllo che la password attuale inserita dall'utente sia la stessa inserita nel database
        if not (bcrypt.checkpw(vecchia_password.encode('utf-8'), password_attuale.encode('utf-8'))):
            return jsonify({'message': 'La password attuale inserita non è valida'}), 401
        
        #Aggiorno la password con la nuova password
        hashed_password = hash_password(nuova_password)
        cur.execute("UPDATE users SET password = %s WHERE id = %s RETURNING id", (hashed_password, user_id,))
        aggiornato = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if aggiornato:
            return jsonify({
                "message": "Password cambiata con successo"
            }), 200
        else:
            return jsonify({'message': 'nessun utente trovato'}), 404
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

#Metodo per eliminare un utente
def deleteUtente(userID):
    try :
        conn = connetti_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (userID,))
        eliminato = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if eliminato:
            return 204
        else:
            return jsonify({'message': 'nessun utente trovato'}), 404
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

#Metodo per ottenere le info di un utente
def getUtente(userID):
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
   