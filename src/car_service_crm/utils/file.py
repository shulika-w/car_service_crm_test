"""Утиліти для збереження файлів, завантажених документів механіків."""

import os
from fastapi import UploadFile

UPLOAD_FOLDER = "uploaded_documents"

def secure_filename(filename: str) -> str:
    return filename.replace(" ", "_").replace("/", "_")

def save_upload_file(upload_file: UploadFile, mechanic_id: int) -> str:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{mechanic_id}_{secure_filename(upload_file.filename)}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path