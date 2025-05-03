import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, 'static', 'uploads')
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static', 'uploads')
