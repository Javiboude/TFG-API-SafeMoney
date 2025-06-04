from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from app.db.database import Base

class Bizum(Base):

    __tablename__ = 'bizums'
    
    id = Column(Integer, primary_key=True, index=True)
    telefono_emisor = Column(String(20), ForeignKey('usuarios.telefono'))
    telefono_receptor = Column(String(20), ForeignKey('usuarios.telefono'))
    cantidad = Column(Float)
    concepto = Column(String(255))
    fecha = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')