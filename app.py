from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import firebase_admin
from firebase_admin import credentials, auth, storage, db
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar app Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

# Obtener la clave privada de Firebase desde las variables de entorno
private_key = os.getenv("FIREBASE_PRIVATE_KEY")

# Inicializar Firebase con las credenciales
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "charsschat",
    "private_key_id": "d259cb17802d8a8d2b1abd4a12f0203e901eeb23",
    "private_key": private_key,  # Usar la clave cargada desde la variable de entorno
    "client_email": "firebase-adminsdk-fbsvc@charsschat.iam.gserviceaccount.com",
    "client_id": "109002188473903551976",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40charsschat.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://charsschat.firebaseio.com/',
    'storageBucket': 'charsschat.appspot.com'
})
bucket = storage.bucket()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------------
# Rutas
# ----------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            session['username'] = email.split('@')[0]
            session['email'] = email
            return redirect('/chat')
        except:
            return 'Usuario no encontrado o error al iniciar sesión'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user(email=email, password=password)
            return redirect('/')
        except:
            return 'Error al registrar usuario'
    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    ref = db.reference('messages')
    messages = ref.get() or {}
    return render_template('chat.html', messages=messages)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ----------------------
# SocketIO Eventos
# ----------------------

@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    username = data['username']
    db.reference('messages').push({
        'username': username,
        'message': message
    })
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)

# Subida de archivos
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)

        blob = bucket.blob(f"uploads/{filename}")
        blob.upload_from_filename(local_path)
        blob.make_public()

        # Enviar el link como mensaje
        username = session.get('username', 'Anónimo')
        db.reference('messages').push({
            'username': username,
            'message': f"<a href='{blob.public_url}' target='_blank'>{filename}</a>"
        })
        socketio.emit('receive_message', {'username': username, 'message': f"<a href='{blob.public_url}' target='_blank'>{filename}</a>"})
        return 'Success'
    return 'Failed'

# ----------------------

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

