from sqlalchemy import Column, Float, Integer, String, TIMESTAMP, ForeignKey
from app.db.database import Base

class Tarjeta(Base):
    
    __tablename__ = "tarjetas"

    id = Column(Integer, primary_key=True, index=True)
    telefono_usuario = Column(String(20), ForeignKey('usuarios.telefono'), nullable=False)
    cuenta_asociada = Column(String(24), ForeignKey('usuarios.iban'), nullable=False)
    numero_tarjeta = Column(String(16), nullable=False, unique=True)
    fecha_caducidad = Column(String(5), nullable=False)
    cvc = Column(String(3), nullable=False)
    tipo = Column(String(20), nullable=False)
    limite_online = Column(Float, nullable=False)
    limite_fisico = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')