from sqlalchemy.orm import Session
from app.models.balanceMensual import BalanceMensual
from datetime import datetime
from app.models.bizum import Bizum
from app.models.transferencia import Transferencia

class TransaccionService:
    def __init__(self, db: Session):
        self.db = db

    def get_balances(self):
        return self.db.query(BalanceMensual).all()

    def create_bizum(self, telefono_emisor: str, telefono_receptor: str, cantidad: float, concepto: str):
        db_bizum = Bizum(
            telefono_emisor=telefono_emisor,
            telefono_receptor=telefono_receptor,
            cantidad=cantidad,
            concepto=concepto,
            fecha=datetime.now()
        )
        self.db.add(db_bizum)
        self.db.commit()
        self.db.refresh(db_bizum)
        return db_bizum

    def create_transferencia(self, iban_emisor: str, iban_receptor: str, cantidad: float, concepto: str):
        db_transferencia = Transferencia(
            iban_emisor=iban_emisor,
            iban_receptor=iban_receptor,
            cantidad=cantidad,
            concepto=concepto,
            fecha=datetime.now()
        )
        self.db.add(db_transferencia)
        self.db.commit()
        self.db.refresh(db_transferencia)
        return db_transferencia