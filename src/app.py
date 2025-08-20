# app.py
from flask import Flask
from flask_socketio import SocketIO
import os

# Importa i router
from routes.rAutenticazione import auth_bp
from routes.rPosizioni import posizioni_bp

# 1. Inizializza l'applicazione Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# 2. Registra i percorsi (Routes)
# Collega il router di autenticazione al prefisso /api/auth
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Collega il router delle posizioni al prefisso /api/posizioni
app.register_blueprint(posizioni_bp, url_prefix='/api/posizioni')

# Codice per le WebSockets
@socketio.on('connect')
def handle_connect():
    print('Client connected to socket')

# 3. Avvia il server
if __name__ == '__main__':
    # Esegue l'applicazione usando il server SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)