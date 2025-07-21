"""Ендпоінти для CRUD-операцій над механіками. Доступ лише для адміністратора."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth
from ..deps import get_db

router = APIRouter(
    prefix="/mechanics",
    tags=["mechanics"]
)

@router.post("/", response_model=schemas.MechanicOut)
def create_mechanic(
    mechanic: schemas.MechanicCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    if crud.get_mechanic_by_login(db, mechanic.login):
        raise HTTPException(status_code=400, detail="Login already exists")
    return crud.create_mechanic(db, mechanic)

@router.get("/", response_model=List[schemas.MechanicOut])
def get_mechanics(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    return crud.get_mechanics(db)

from fastapi import status

@router.post("/login")
def mechanic_login(
    data: schemas.MechanicLogin,
    db: Session = Depends(get_db)
):
    mech = auth.authenticate_mechanic(db, data.login, data.password)
    if not mech:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")
    access_token = auth.create_access_token(data={"sub": mech.login, "role": mech.role.value})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{mechanic_id}", response_model=schemas.MechanicOut)
def get_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    mech = crud.get_mechanic(db, mechanic_id)
    if mech is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return mech

@router.put("/{mechanic_id}", response_model=schemas.MechanicOut)
def update_mechanic(
    mechanic_id: int,
    mechanic_update: schemas.MechanicUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    mech = crud.update_mechanic(db, mechanic_id, mechanic_update)
    if mech is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return mech

@router.delete("/{mechanic_id}")
def delete_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    mech = crud.delete_mechanic(db, mechanic_id)
    if mech is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return {"ok": True}