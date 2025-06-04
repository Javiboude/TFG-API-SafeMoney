from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    telefono = Column(String, unique=True, index=True)
    password = Column(String)
    dinero = Column(Float, default=0.0) 
    iban = Column(String(24), unique=True, index=True)
