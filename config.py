import os

class Config:
    SECRET_KEY = 'hello123'  # Replace with a strong secret key
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/gallery_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_DEFAULT_DEST = os.path.join(os.getcwd(), 'static', 'uploads')
    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'static', 'uploads')