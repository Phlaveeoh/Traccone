from flask import Blueprint

# Importa la logica del controller
from controllers.cAutenticazione import login, register
from servizi.servizioAutenticatore import valida_token

# Crea un Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
#@valida_token
def handle_login():
    return login()

@auth_bp.route('/register', methods=['POST'])
#@valida_token
def handle_register():
    return register()