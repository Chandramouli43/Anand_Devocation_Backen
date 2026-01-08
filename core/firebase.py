import firebase_admin
from firebase_admin import credentials

from core.config import FIREBASE_CREDENTIALS_PATH

if FIREBASE_CREDENTIALS_PATH and not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
