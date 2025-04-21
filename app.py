from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import firebase_admin
from firebase_admin import credentials, db
import os

# Inicializar app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Clave secreta para la sesión
app.config['SESSION_TYPE'] = 'filesystem'

# Inicializar SocketIO con CORS habilitado
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Configuración de Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://charsschat-default-rtdb.firebaseio.com/'
})

# Ruta de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')
        if username:
            session['username'] = username  # Guardar el nombre del usuario en la sesión
            return redirect(url_for('chat'))
    return render_template('login.html')

# Ruta de chat
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirige al login
    # Leer mensajes desde Firebase
    ref = db.reference('/messages')
    messages = ref.get() or {}

    if 'inicio' in messages:
        del messages['inicio']  # Eliminar mensaje de inicio si existe

    return render_template('chat.html', messages=messages)

# Evento SocketIO para mensajes
@socketio.on('send_message')
def handle_send_message_event(data):
    ref = db.reference('/messages')
    new_msg = ref.push()
    new_msg.set({
        'username': data['username'],
        'message': data['message']
    })
    emit('receive_message', data, broadcast=True)

# Iniciar servidor
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
