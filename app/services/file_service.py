"""
File upload service — handles secure uploads for all types of files.
"""
import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_upload(file_obj, subfolder, allowed_extensions):
    """
    Save an uploaded file to the uploads/<subfolder> directory.
    Returns (saved_filename, original_filename) or raises ValueError.
    """
    if not file_obj or file_obj.filename == '':
        raise ValueError("No file selected.")

    original_name = secure_filename(file_obj.filename)
    if not allowed_file(original_name, allowed_extensions):
        raise ValueError(f"File type not allowed. Allowed: {', '.join(allowed_extensions)}")

    ext = original_name.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    upload_root = current_app.config['UPLOAD_FOLDER']
    dest_dir = os.path.join(upload_root, subfolder)
    os.makedirs(dest_dir, exist_ok=True)

    full_path = os.path.join(dest_dir, unique_name)
    file_obj.save(full_path)
    return unique_name, original_name


def delete_upload(subfolder, filename):
    """Delete a previously saved upload file."""
    if not filename:
        return
    upload_root = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    full_path = os.path.join(upload_root, subfolder, filename)
    if os.path.exists(full_path):
        os.remove(full_path)
