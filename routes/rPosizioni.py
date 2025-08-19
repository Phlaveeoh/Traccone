from flask import Blueprint, jsonify

# Importa la logica del controller
from controllers.cPosizioni import salvaPosizione, getPosizioni, salvaBulk
from servizi.servizioAutenticatore import valida_token

# Crea un Blueprint
posizioni_bp = Blueprint('location', __name__)

# Definizione del percorso (route) per salvare una posizione
# Questo endpoint accetta solo richieste POST e usa il middleware di autenticazione
#/api/posizioni/save 
@posizioni_bp.route('/save', methods=['POST'])
@valida_token
def handle_save(user_id):
    return salvaPosizione(user_id)

# Definizione del percorso per ottenere lo storico delle posizioni di un utente
@posizioni_bp.route('/<int:user_id>', methods=['GET'])
@valida_token
def handle_get_positions(current_user_id, user_id):
    # Esempio di logica di autorizzazione:
    # L'utente può accedere solo ai propri dati.
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return getPosizioni(user_id)

@posizioni_bp.route('/bulk', methods=['POST'])
@valida_token
def handle_save_bulk(user_id):
    return salvaBulk(user_id)