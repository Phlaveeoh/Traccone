# app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Definizione di un endpoint URL.
# Questo endpoint risponderà alle richieste GET sulla root ('/')
@app.route('/')
def home():
    # Restituisce una risposta in formato JSON
    return jsonify({"message": "Il server Flask è in esecuzione!"})

# Avvia l'applicazione in modalità di sviluppo
if __name__ == '__main__':
    # La modalità di debug è utile per lo sviluppo, riavvia il server
    # automaticamente quando salvi le modifiche
    app.run(debug=True, host='0.0.0.0', port=5000)