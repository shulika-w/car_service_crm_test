"""Ендпоінти для завантаження та перегляду документів механіків."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth
from ..deps import get_db
from ..utils.file import save_upload_file

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.post("/", response_model=schemas.DocumentOut)
def upload_document(
    mechanic_id: int = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    file_path = save_upload_file(file, mechanic_id)
    return crud.create_document(db, mechanic_id, type, file_path)

@router.get("/by_mechanic/{mechanic_id}", response_model=List[schemas.DocumentOut])
def get_documents_by_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    return crud.get_documents_by_mechanic(db, mechanic_id)

@router.get("/{document_id}", response_model=schemas.DocumentOut)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    doc = crud.get_document(db, document_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    doc = crud.delete_document(db, document_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"ok": True}