from sqlalchemy.orm import Session
from datetime import datetime
from app.models.movimiento import Movimiento

class MovimientoService:
    def __init__(self, db: Session):
        self.db = db

    def get_movimientos_usuario(self, usuario_id: int, limit: int = 10):
        return self.db.query(Movimiento).filter(
            Movimiento.usuario_id == usuario_id
        ).order_by(Movimiento.fecha.desc()).limit(limit).all()

    def create_movimiento_usuario(self, usuario_id: int, motivo: str, lugar: str, cantidad: float, es_positiva: bool):
        db_movimiento = Movimiento(
            usuario_id=usuario_id,
            motivo=motivo,
            lugar=lugar,
            cantidad=cantidad,
            es_positiva=es_positiva,
            fecha=datetime.now()
        )
        self.db.add(db_movimiento)
        self.db.commit()
        self.db.refresh(db_movimiento)
        return db_movimiento