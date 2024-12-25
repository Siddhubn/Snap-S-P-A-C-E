from flask import current_app
import os

def create_upload_directory():
    """Ensure the upload directory exists."""
    upload_path = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

create_upload_directory()
