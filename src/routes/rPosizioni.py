from flask import Blueprint, jsonify, request

#Importa la logica del controller
from controllers.cPosizioni import salvaPosizione, getPath, salvaBulk, getLastPosition
from servizi.servizioAutenticatore import valida_token

#Crea un Blueprint
posizioni_bp = Blueprint('location', __name__)

#/api/posizioni/save 
@posizioni_bp.route('/save', methods=['POST'])
@valida_token
def handle_save(user_id):
    return salvaPosizione(user_id)

#api/posizioni/bulk
@posizioni_bp.route('/bulk', methods=['POST'])
@valida_token
def handle_save_bulk(user_id):
    return salvaBulk(user_id)

#api/posizioni/<user_id>/lastPosition
@posizioni_bp.route('/<int:user_id>/lastPosition', methods=['GET'])
@valida_token
def handle_get_last_position(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return getLastPosition(user_id)

#api/posizioni/<user_id>?data=YYYY-MM-DD
@posizioni_bp.route('/<int:user_id>', methods=['GET'])
@valida_token
def handle_get_path(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    data = request.args.get('data')
    if not data:
        return jsonify({"errore": "Parametro 'data' mancante"}), 400
    return getPath(user_id, data)