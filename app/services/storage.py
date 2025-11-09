import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")

def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_local(upload_file: UploadFile) -> str:
    ensure_upload_dir()
    ext = os.path.splitext(upload_file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(dest_path, "wb") as f:
        content = upload_file.file.read()
        f.write(content)

    #return path relative to project root which is stored in PostgreSQL
    return f"uploads/{unique_name}"