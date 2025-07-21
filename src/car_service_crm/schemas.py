"""Pydantic-схеми для валідації, серіалізації та десеріалізації даних в API."""

from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, Literal

UserRole = Literal["admin", "customer"]
MechanicRole = Literal["admin", "mechanic"]

# ---------------- USERS ----------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRoleUpdate(BaseModel):
    role: UserRole

# ---------------- CARS ----------------

class CarBase(BaseModel):
    brand: str
    model: str
    year: int
    plate_number: str
    vin: str

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass

class CarOut(CarBase):
    car_id: int
    user_id: int

    class Config:
        from_attributes = True

# ---------------- SERVICES ----------------

class ServiceBase(BaseModel):
    name: str
    description: str
    price: int
    duration: int

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    service_id: int

    class Config:
        from_attributes = True

# ---------------- MECHANICS ----------------

class MechanicCreate(BaseModel):
    name: str
    birth_date: date
    login: str
    password: str
    role: MechanicRole
    position: str

class MechanicLogin(BaseModel):
    login: str
    password: str

class MechanicUpdate(BaseModel):
    password: Optional[str] = None
    role: Optional[MechanicRole] = None

class MechanicOut(BaseModel):
    mechanic_id: int
    name: str
    birth_date: date
    login: str
    role: MechanicRole
    position: str

    class Config:
        from_attributes = True

# ---------------- DOCUMENTS ----------------

class DocumentBase(BaseModel):
    type: str

class DocumentCreate(DocumentBase):
    pass  # файл приймається окремо через FormData

class DocumentOut(DocumentBase):
    document_id: int
    mechanic_id: int
    file_path: str

    class Config:
        from_attributes = True

# ---------------- APPOINTMENTS ----------------

class AppointmentBase(BaseModel):
    car_id: int
    service_id: int
    appointment_date: datetime

class AppointmentCreate(AppointmentBase):
    mechanic_id: Optional[int] = None
    status: Optional[str] = "created"

class AppointmentUpdate(BaseModel):
    mechanic_id: Optional[int] = None
    status: Optional[str] = None
    appointment_date: Optional[datetime] = None

class AppointmentOut(AppointmentBase):
    appointment_id: int
    user_id: int
    mechanic_id: Optional[int] = None
    status: str

    class Config:
        from_attributes = True