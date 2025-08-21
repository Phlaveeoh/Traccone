from flask import request, jsonify
import traceback
import psycopg2.extras
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


def getPath(user_id, data):
    
    try:
        conn = connetti_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
            # Query sicura per ottenere latitudine, longitudine e timestamp
        # della traiettoria di un utente per una data specifica.
        query = """
            SELECT
                ST_X(location) AS longitudine,
                ST_Y(location) AS latitudine,
                timestamp,
                user_id
            FROM
                locations
            WHERE
                user_id = %s AND timestamp::date = %s
            ORDER BY
                timestamp ASC;
        """
        
        cur.execute(query, (user_id, data))
        positions = cur.fetchall()
              
        cur.close()
        conn.close()
        
        # Converte i risultati in GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        if positions:
            for pos in positions:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [pos['longitudine'], pos['latitudine']]
                    },
                    "properties": {
                        "timestamp": pos['timestamp'].isoformat(),
                        "user_id": pos['user_id']
                    }
                }
                geojson['features'].append(feature)
        
        # Restituisce l'oggetto GeoJSON e il codice di stato 200 (OK)
        return jsonify(geojson), 200
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

def getLastPosition(user_id):
    try :
        conn = connetti_db()
        cur = conn.cursor()

        cur.execute("SELECT ST_X(location) AS longitudine, ST_Y(location) AS latitudine FROM locations WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1;", (user_id,))
        last_position = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if last_position:
            longitudine = last_position[0]
            latitudine = last_position[1]
            
            return jsonify({
                'longitudine': longitudine,
                'latitudine': latitudine
            }), 200
        else:
            return jsonify({'message': 'Nessuna posizione trovata'}), 404
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500