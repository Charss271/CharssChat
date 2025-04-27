import firebase_admin
from firebase_admin import credentials, auth, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://charsschat.firebaseio.com/',
    'storageBucket': 'charsschat.appspot.com'
})
