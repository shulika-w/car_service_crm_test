"""Ендпоінти для керування автомобілями клієнтів."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth
from ..deps import get_db

router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

@router.post("/", response_model=schemas.CarOut)
def create_car(
    car: schemas.CarCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    return crud.create_car(db, car, user_id=current_user.user_id)

@router.get("/", response_model=List[schemas.CarOut])
def get_my_cars(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    return crud.get_cars_by_user(db, user_id=current_user.user_id)

@router.get("/{car_id}", response_model=schemas.CarOut)
def get_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    car = crud.get_car(db, car_id)
    if car is None or car.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.put("/{car_id}", response_model=schemas.CarOut)
def update_car(
    car_id: int,
    car_update: schemas.CarUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    car = crud.update_car(db, car_id, car_update, user_id=current_user.user_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found or no access")
    return car

@router.delete("/{car_id}")
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    car = crud.delete_car(db, car_id, user_id=current_user.user_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found or no access")
    return {"ok": True}