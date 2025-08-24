from flask import Blueprint, jsonify, request

# Importa la logica del controller
from controllers.cPosizioni import salvaPosizione, getPath, salvaBulk, getLastPosition
from servizi.servizioAutenticatore import valida_token

# Crea un Blueprint
utente_bp = Blueprint('utenti', __name__)


#/api/posizioni/save 
@utente_bp.route('/<int:user_id>/update', methods=['PATCH'])
@valida_token
def handle_update(currentUserId, userID):
    if currentUserId != userID: 
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return salvaPosizione(userID)

@utente_bp.route('/<int:user_id>/delete', methods=['DELETE'])
@valida_token
def handle_delete(currentUserId, userID):
    if currentUserId != userID: 
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return eliminaUtente(userID)

@utente_bp.route('/<int:user_id>', methods=['GET'])
@valida_token
def handle_visualization(currentUserId, userID):
    if currentUserId != userID: 
        return jsonify({"errore": "Non sei autorizzato ad accedere a questo contenuto"}), 403
    return prendiUtente(userID) 