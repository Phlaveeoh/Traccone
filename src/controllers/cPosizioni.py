from flask import request, jsonify
import traceback
import psycopg2.extras
from servizi.servizioDB import connetti_db

def salvaPosizione(user_id):
    '''
    Salva la posizione di un utente nel database.
    '''
    #Prende i dati JSON dalla richiesta
    data = request.get_json()
    longitudine = data.get('longitudine')
    latitudine = data.get('latitudine')
    
    #Controlla che longitudine e latitudine siano stati forniti altrimenti ritorna un errore
    if not all([longitudine, latitudine]):
        return jsonify({'error': 'Mancano la longitudine o la latitudine'}), 400

    try :
        #Connessione al database
        conn = connetti_db()
        cur = conn.cursor()
        
        #Inserisce la posizione nel database
        cur.execute("INSERT INTO locations (user_id, location) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));", (user_id, longitudine, latitudine))
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Restituisce una risposta di successo
        return jsonify({'message': 'Posizione salvata con successo'}), 201
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


def salvaBulk(user_id):
    '''
    Salva in bulk le posizioni di un utente nel database.
    '''
    #Prende i dati JSON dalla richiesta
    posizioni = request.get_json()
    
    #Verifica che i dati siano una lista
    if not isinstance(posizioni, list):
        return jsonify({'error': 'Il corpo della richiesta deve essere un elenco di posizioni'}), 400
    
    #Se la lista è vuota 
    if not posizioni:
        return jsonify({'message': 'Non ci sono posizioni da salvare'}), 200
    
    try:
        #Connessione al database
        conn = connetti_db()
        cur = conn.cursor()

        #Preparazione dei dati per l'inserimento multiplo
        datiDaInserire = [] #Creo l'array dei dati da inserire
        for posizione in posizioni: #Per ogni posizione nell'array delle posizioni
            #Controlla che longitudine, latitudine e timestamp siano stati forniti altrimenti salta questa posizione
            if not all([posizione['longitudine'], posizione['latitudine'], posizione['timestamp']]):
                continue
            #Aggiunge la tupla (user_id, longitudine, latitudine, timestamp) all'array dei dati da inserire
            datiDaInserire.append((user_id, posizione['longitudine'], posizione['latitudine'], posizione['timestamp']))

        #Query per l'inserimento multiplo
        query = """
            INSERT INTO locations (user_id, location, timestamp) 
            VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s);
        """
        
        #executemany per un'inserimento ottimizzato di tutte le queries create
        cur.executemany(query, datiDaInserire)
        
        conn.commit()
        cur.close()
        conn.close()
        
        #Restituisce una risposta di successo
        return jsonify({'message': 'Posizioni salvate con successo'}), 201

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


def getPath(user_id, data):
    '''
    Ottiene la traiettoria di un utente per una data specifica.\n
    Restituisce i dati in formato GeoJSON.
    '''
    try:
        #Connessione al database
        conn = connetti_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        #Query per ottenere latitudine, longitudine e timestamp della traiettoria di un utente per una data specifica.
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
        
        #Se ci sono posizioni, le aggiunge al GeoJSON
        if positions:
            for pos in positions: #Per ogni posizione trovata
                #Crea una feature GeoJSON
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
                #Aggiunge la feature al GeoJson
                geojson['features'].append(feature)
        
        #Restituisce l'oggetto GeoJSON e il codice di stato 200 (OK)
        return jsonify(geojson), 200
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


def getLastPosition(user_id):
    '''
    Ottiene l'ultima posizione nota di un utente.
    '''
    try :
        #Connessione al database
        conn = connetti_db()
        cur = conn.cursor()

        #Query per ottenere l'ultima posizione di un utente
        cur.execute("SELECT ST_X(location) AS longitudine, ST_Y(location) AS latitudine FROM locations WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1;", (user_id,))
        last_position = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()
        
        #Se è stata trovata una posizione
        if last_position:
            longitudine = last_position[0]
            latitudine = last_position[1]
            
            return jsonify({
                'longitudine': longitudine,
                'latitudine': latitudine
            }), 200
        else: #Se non è stata trovata nessuna posizione
            return jsonify({'message': 'Nessuna posizione trovata'}), 404
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500