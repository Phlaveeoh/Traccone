from flask import Flask
from flask_socketio import SocketIO

#Importa i router
from routes.rAutenticazione import auth_bp
from routes.rPosizioni import posizioni_bp
from routes.rUtente import utente_bp

#Inizializza l'applicazione Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

#Registra i percorsi (Routes)
#Collega il router di autenticazione al prefisso /api/auth
app.register_blueprint(auth_bp, url_prefix='/api/auth')

#Collega il router delle posizioni al prefisso /api/posizioni
app.register_blueprint(posizioni_bp, url_prefix='/api/posizioni')

#Collega il router delle posizioni al prefisso /api/utenti
app.register_blueprint(utente_bp, url_prefix='/api/utenti')

#Avvia il server
if __name__ == '__main__':
    #Esegue l'applicazione usando il server SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)