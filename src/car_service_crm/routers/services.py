"""Ендпоінти для CRUD-операцій над послугами. Доступ лише для адміністратора."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth
from ..deps import get_db

router = APIRouter(
    prefix="/services",
    tags=["services"]
)

@router.post("/", response_model=schemas.ServiceOut)
def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    return crud.create_service(db, service)

@router.get("/", response_model=List[schemas.ServiceOut])
def get_services(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    return crud.get_services(db)

@router.get("/{service_id}", response_model=schemas.ServiceOut)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    service = crud.get_service(db, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=schemas.ServiceOut)
def update_service(
    service_id: int,
    service_update: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    service = crud.update_service(db, service_id, service_update)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    service = crud.delete_service(db, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"ok": True}