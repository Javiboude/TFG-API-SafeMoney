from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from app.db.database import Base

class Contacto(Base):

    __tablename__ = "contactos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nombre_contacto = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')