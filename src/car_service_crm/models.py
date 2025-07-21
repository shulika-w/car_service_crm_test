"""ORM-моделі SQLAlchemy для всіх сутностей згідно з вимогами ТЗ."""

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from .db import Base
import enum

# Enums 
class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"

class MechanicRole(str, enum.Enum):
    admin = "admin"
    mechanic = "mechanic"

# Users 
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(32), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)

# Cars
class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    brand = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    year = Column(Integer, nullable=False)
    plate_number = Column(String(32), unique=True, nullable=False)
    vin = Column(String(16), unique=True, nullable=False)

# Services
class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  # тривалість у хвилинах

# Mechanics
class Mechanic(Base):
    __tablename__ = "mechanics"

    mechanic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    birth_date = Column(Date, nullable=False)
    login = Column(String(64), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    role = Column(Enum(MechanicRole), default=MechanicRole.mechanic, nullable=False)
    position = Column(String(64), nullable=False)

# Documents
class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=False)
    type = Column(String(128), nullable=False)        # паспорт, ІПН, диплом, договір
    file_path = Column(String(255), nullable=False)   # шлях до файлу на диску

# Appointments
class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.car_id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=True)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(255), default="created", nullable=False)  # created, confirmed, canceled, completed