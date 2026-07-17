"""
Upload Blueprint — handles chunked file uploading.
"""
import os
import shutil
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.routes.auth import login_required

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload-chunk', methods=['POST'])
@login_required
def upload_chunk():
    file = request.files.get('file')
    chunk_index = int(request.form.get('chunkIndex', 0))
    total_chunks = int(request.form.get('totalChunks', 1))
    file_identifier = request.form.get('fileIdentifier', '').strip()
    filename = request.form.get('filename', '').strip()

    if not file or not file_identifier or not filename:
        return jsonify({'error': 'Missing required upload parameters'}), 400

    # Create secure temporary directory for this upload ID
    temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', file_identifier)
    os.makedirs(temp_dir, exist_ok=True)

    # Save current chunk file
    chunk_filename = f"chunk_{chunk_index}"
    chunk_filepath = os.path.join(temp_dir, chunk_filename)
    file.save(chunk_filepath)

    # Check if all chunks are uploaded
    try:
        uploaded_chunks = len(os.listdir(temp_dir))
    except Exception as e:
        current_app.logger.error(f"Failed to list temp upload folder: {e}")
        return jsonify({'error': 'Failed during chunk check'}), 500

    if uploaded_chunks == total_chunks:
        # Reassemble
        sec_name = secure_filename(filename)
        # Ensure unique filename to prevent collisions while preserving extension
        ext = os.path.splitext(sec_name)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        final_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)

        try:
            with open(final_filepath, 'wb') as merged_file:
                for i in range(total_chunks):
                    curr_chunk_path = os.path.join(temp_dir, f"chunk_{i}")
                    with open(curr_chunk_path, 'rb') as source_chunk:
                        merged_file.write(source_chunk.read())
            
            # Cleanup temp directory
            shutil.rmtree(temp_dir)
            return jsonify({
                'status': 'completed',
                'filename': unique_name,
                'original_name': sec_name
            })
        except Exception as e:
            current_app.logger.error(f"Failed to merge chunks: {e}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return jsonify({'error': 'Failed to reassemble chunks'}), 500

    return jsonify({'status': 'chunk_saved', 'chunkIndex': chunk_index})
