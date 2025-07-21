"""Ендпоінти для запису на обслуговування, призначення механіків, перегляду історії."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth
from ..deps import get_db
from ..utils.email import send_email_async

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

# Створення запису (тільки для авторизованого користувача)
@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(
    data: schemas.AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    app = crud.create_appointment(db, user_id=current_user.user_id, data=data)
    # Асинхронна відправка email (наприклад, на current_user.email)
    subject = "Підтвердження запису"
    body = f"Ваша заявка на обслуговування прийнята (ID: {app.appointment_id})"
    background_tasks.add_task(send_email_async, current_user.email, subject, body)
    return app

# Перегляд своїх записів
@router.get("/", response_model=List[schemas.AppointmentOut])
def get_my_appointments(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_user)
):
    return crud.get_appointments_by_user(db, current_user.user_id)

# Для механіка — свої призначення (за mechanic_id)
@router.get("/mechanic/{mechanic_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)  # Для простоти — лише адмін
):
    return crud.get_appointments_by_mechanic(db, mechanic_id)

# Для адміністратора — всі записи
@router.get("/all", response_model=List[schemas.AppointmentOut])
def get_all_appointments(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    return crud.get_all_appointments(db)

# Оновлення статусу/механіка (адмін)
@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(
    appointment_id: int,
    data: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    app = crud.update_appointment(db, appointment_id, data)
    if app is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return app

# Видалення (адмін)
@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_active_admin)
):
    app = crud.delete_appointment(db, appointment_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"ok": True}