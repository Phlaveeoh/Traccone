from flask import Blueprint

#Importa la logica del controller
from controllers.cAutenticazione import login, register

#Crea un Blueprint
auth_bp = Blueprint('auth', __name__)

#api/auth/login
@auth_bp.route('/login', methods=['POST'])
def handle_login():
    return login()

#api/auth/register
@auth_bp.route('/register', methods=['POST'])
def handle_register():
    return register()