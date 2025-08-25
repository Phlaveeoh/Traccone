from flask import Blueprint, jsonify, request

# Importa la logica del controller
from controllers.cUtente import updateUtente, cambiaPassword, deleteUtente, getUtente
from servizi.servizioAutenticatore import valida_token

# Crea un Blueprint
utente_bp = Blueprint('utenti', __name__)


#/api/utenti/<user_id>/update
@utente_bp.route('/<int:user_id>/update', methods=['PATCH'])
@valida_token
def handle_update(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return updateUtente(user_id)

#/api/utenti/<user_id>/cambiaPassword
@utente_bp.route('/<int:user_id>/cambiaPassword', methods=['PATCH'])
@valida_token
def handle_change_password(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return cambiaPassword(user_id)

#/api/utenti/<user_id>/delete
@utente_bp.route('/<int:user_id>/delete', methods=['DELETE'])
@valida_token
def handle_delete(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return deleteUtente(user_id)

#/api/utenti/<user_id>
@utente_bp.route('/<int:user_id>', methods=['GET'])
@valida_token
def handle_visualization(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return getUtente(user_id)