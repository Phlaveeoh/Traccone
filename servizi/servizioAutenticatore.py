import jwt
import os

def hash_password(password):
    pass

def crea_token(user_id):
    """
    Crea un token JWT per l'utente.
    """
    payload = {'user_id': user_id}
    return jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')

def valida_token():
    pass