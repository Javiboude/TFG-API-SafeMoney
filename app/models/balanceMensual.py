from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class BalanceMensual(Base):
    
    __tablename__ = "balances_mensuales"
    
    id = Column(Integer, primary_key=True, index=True)
    mes = Column(String(2), nullable=False)
    ingresos = Column(Float, nullable=False)
    gastos = Column(Float, nullable=False)