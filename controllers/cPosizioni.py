from flask import request, jsonify
import traceback
from servizi.servizioDB import connetti_db

def salvaPosizione(user_id):
    
    data = request.get_json()
    longitudine = data.get('longitudine')
    latitudine = data.get('latitudine')
    
    if not all([longitudine, latitudine]):
        return jsonify({'error': 'Missing longitude or latitude'}), 400

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