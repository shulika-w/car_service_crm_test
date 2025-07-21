"""CRUD-операції для роботи з усіма сутностями: користувачі, авто, послуги, механіки, документи, записи."""

from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash


# USERS
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    is_first_user = db.query(models.User).count() == 0
    role = models.UserRole.admin if is_first_user else models.UserRole.customer
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_role(db: Session, user_id: int, role: schemas.UserRole):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# CARS
def create_car(db: Session, car: schemas.CarCreate, user_id: int):
    db_car = models.Car(**car.dict(), user_id=user_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def get_cars_by_user(db: Session, user_id: int):
    return db.query(models.Car).filter(models.Car.user_id == user_id).all()

def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.car_id == car_id).first()

def update_car(db: Session, car_id: int, car_update: schemas.CarUpdate, user_id: int):
    car = db.query(models.Car).filter(models.Car.car_id == car_id, models.Car.user_id == user_id).first()
    if car:
        for var, value in car_update.dict().items():
            setattr(car, var, value)
        db.commit()
        db.refresh(car)
    return car

def delete_car(db: Session, car_id: int, user_id: int):
    car = db.query(models.Car).filter(models.Car.car_id == car_id, models.Car.user_id == user_id).first()
    if car:
        db.delete(car)
        db.commit()
    return car


# SERVICES
def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_services(db: Session):
    return db.query(models.Service).all()

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.service_id == service_id).first()

def update_service(db: Session, service_id: int, service_update: schemas.ServiceUpdate):
    service = db.query(models.Service).filter(models.Service.service_id == service_id).first()
    if service:
        for var, value in service_update.dict().items():
            setattr(service, var, value)
        db.commit()
        db.refresh(service)
    return service

def delete_service(db: Session, service_id: int):
    service = db.query(models.Service).filter(models.Service.service_id == service_id).first()
    if service:
        db.delete(service)
        db.commit()
    return service


# MECHANICS
def create_mechanic(db: Session, mechanic: schemas.MechanicCreate):
    db_mech = models.Mechanic(
        name=mechanic.name,
        birth_date=mechanic.birth_date,
        login=mechanic.login,
        password=get_password_hash(mechanic.password),
        role=mechanic.role,
        position=mechanic.position
    )
    db.add(db_mech)
    db.commit()
    db.refresh(db_mech)
    return db_mech

def get_mechanic_by_login(db: Session, login: str):
    return db.query(models.Mechanic).filter(models.Mechanic.login == login).first()

def get_mechanics(db: Session):
    return db.query(models.Mechanic).all()

def get_mechanic(db: Session, mechanic_id: int):
    return db.query(models.Mechanic).filter(models.Mechanic.mechanic_id == mechanic_id).first()

def update_mechanic(db: Session, mechanic_id: int, mechanic_update: schemas.MechanicUpdate):
    mech = db.query(models.Mechanic).filter(models.Mechanic.mechanic_id == mechanic_id).first()
    if mech:
        for var, value in mechanic_update.dict(exclude_unset=True).items():
            if var == "password" and value:
                value = get_password_hash(value)
            setattr(mech, var, value)
        db.commit()
        db.refresh(mech)
    return mech

def delete_mechanic(db: Session, mechanic_id: int):
    mech = db.query(models.Mechanic).filter(models.Mechanic.mechanic_id == mechanic_id).first()
    if mech:
        db.delete(mech)
        db.commit()
    return mech

# DOCUMENTS
def create_document(db: Session, mechanic_id: int, doc_type: str, file_path: str):
    db_doc = models.Document(
        mechanic_id=mechanic_id,
        type=doc_type,
        file_path=file_path
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_documents_by_mechanic(db: Session, mechanic_id: int):
    return db.query(models.Document).filter(models.Document.mechanic_id == mechanic_id).all()

def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.document_id == document_id).first()

def delete_document(db: Session, document_id: int):
    doc = db.query(models.Document).filter(models.Document.document_id == document_id).first()
    if doc:
        db.delete(doc)
        db.commit()
    return doc

# APPOINTMENTS
def create_appointment(db: Session, user_id: int, data: schemas.AppointmentCreate):
    db_app = models.Appointment(
        user_id=user_id,
        car_id=data.car_id,
        service_id=data.service_id,
        mechanic_id=data.mechanic_id,
        appointment_date=data.appointment_date,
        status=data.status or "created"
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_appointments_by_user(db: Session, user_id: int):
    return db.query(models.Appointment).filter(models.Appointment.user_id == user_id).all()

def get_appointments_by_mechanic(db: Session, mechanic_id: int):
    return db.query(models.Appointment).filter(models.Appointment.mechanic_id == mechanic_id).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id).first()

def get_all_appointments(db: Session):
    return db.query(models.Appointment).all()

def update_appointment(db: Session, appointment_id: int, update: schemas.AppointmentUpdate):
    app = db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id).first()
    if app:
        for var, value in update.dict(exclude_unset=True).items():
            setattr(app, var, value)
        db.commit()
        db.refresh(app)
    return app

def delete_appointment(db: Session, appointment_id: int):
    app = db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id).first()
    if app:
        db.delete(app)
        db.commit()
    return app