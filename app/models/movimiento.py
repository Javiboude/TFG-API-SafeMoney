from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey
from app.db.database import Base

class Movimiento(Base):

    __tablename__ = 'movimientos'
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    motivo = Column(String(255), nullable=False)
    lugar = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    es_positiva = Column(Boolean, nullable=False)
    fecha = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')