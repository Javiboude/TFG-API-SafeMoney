from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from app.db.database import Base

class Transferencia(Base):

    __tablename__ = 'transferencias'
    
    id = Column(Integer, primary_key=True, index=True)
    iban_emisor = Column(String(24), ForeignKey('usuarios.iban'))
    iban_receptor = Column(String(24), ForeignKey('usuarios.iban'))
    cantidad = Column(Float)
    concepto = Column(String(255))
    fecha = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')