from flask import Blueprint

# Importa la logica del controller
from controllers.cAutenticazione import login, register
from servizi.servizioAutenticatore import valida_token

# Crea un Blueprint
auth_bp = Blueprint('auth', __name__)

# Definizione del percorso (route) per salvare una posizione
# Questo endpoint accetta solo richieste POST e usa il middleware di autenticazione
#/api/posizioni/save 
@auth_bp.route('/login', methods=['POST'])
#@valida_token
def handle_login():
    return login()

# Definizione del percorso per ottenere lo storico delle posizioni di un utente
@auth_bp.route('/register', methods=['POST'])
#@valida_token
def handle_register():
    return register()