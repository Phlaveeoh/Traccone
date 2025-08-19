from flask import request, jsonify
import traceback
from servizi.servizioDB import connetti_db

def salvaPosizione(user_id):
    
    data = request.get_json()
    longitudine = data.get('longitudine')
    latitudine = data.get('latitudine')
    
    if not all([longitudine, latitudine]):
        return jsonify({'error': 'Mancano la longitudine o la latitudine'}), 400

    try :
        conn = connetti_db()
        cur = conn.cursor()
        
        cur.execute("INSERT INTO locations (user_id, location) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));", (user_id, longitudine, latitudine))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Posizione salvata con successo'}), 201
        
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

def getPosizioni(user_id):
    return jsonify({'message': 'Not implemented yet'}), 501

def salvaBulk(user_id):
    posizioni = request.get_json()
    
    # Verifica che i dati siano una lista
    if not isinstance(posizioni, list):
        return jsonify({'error': 'Il corpo della richiesta deve essere un elenco di posizioni'}), 400
    
    # Se la lista è vuota 
    if not posizioni:
        return jsonify({'message': 'Non ci sono posizioni da salvare'}), 200
    
    try:
        conn = connetti_db()
        cur = conn.cursor()

        # Preparazione dei dati per l'inserimento multiplo
        datiDaInserire = []
        for posizione in posizioni:
            if not all([posizione['longitudine'], posizione['latitudine'], posizione['timestamp']]):
                continue
            datiDaInserire.append((user_id, posizione['longitudine'], posizione['latitudine'], posizione['timestamp']))

        query = """
            INSERT INTO locations (user_id, location, timestamp) 
            VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s);
        """
        
        # Uso di executemany per un'inserimento ottimizzato
        cur.executemany(query, datiDaInserire)
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Posizioni salvate con successo'}), 201

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500
        