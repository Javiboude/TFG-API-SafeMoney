from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.services.movimientoService import MovimientoService

router = APIRouter(prefix="", tags=["Movimientos"])

@router.get("/ultimos-movimientos/{user_id}")
def get_movimientos_usuario(user_id: int, db: Session = Depends(database.get_db)):
    service = MovimientoService(db)
    movimientos = service.get_movimientos_usuario(user_id)
    return {"movimientos": [
        {
            "id": mov.id,
            "motivo": mov.motivo,
            "lugar": mov.lugar,
            "cantidad": mov.cantidad,
            "es_positiva": mov.es_positiva,
            "fecha": mov.fecha.isoformat()
        } for mov in movimientos
    ]}