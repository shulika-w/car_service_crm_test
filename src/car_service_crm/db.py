"""Налаштування SQLAlchemy: підключення до БД, базовий engine, сесія та declarative_base."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite [dev]
# SQLALCHEMY_DATABASE_URL = "sqlite:///./car_service_crm.db"

# engine = create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, future=True
#)

# MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://crm_user:crm_pass@localhost:3306/car_service_crm"

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()