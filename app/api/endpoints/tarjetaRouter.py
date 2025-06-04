from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.db.database as database
from app.models.tarjeta import Tarjeta
from app.models.usuario import Usuario
from app.schemas.tarjetaSchema import InfoTarjetaResponse, ActualizarLimitesRequest, LimitesResponse
from app.db.database import get_db


router = APIRouter(prefix="", tags=["Tarjetas"])

@router.get("/info-tarjeta/{telefono}", response_model=InfoTarjetaResponse)
async def get_info_tarjeta(telefono: str, db: Session = Depends(database.get_db)):
    tarjeta = db.query(Tarjeta).filter(Tarjeta.telefono_usuario == telefono).first()
    usuario = db.query(Usuario).filter(Usuario.telefono == telefono).first()
    
    if not tarjeta or not usuario:
        raise HTTPException(status_code=404, detail="Datos no encontrados")

    return {
        "saldoCuenta": str(usuario.dinero),
        "titular": usuario.nombre,
        "cuentaAsociada": tarjeta.cuenta_asociada,
        "fechaCaducidad": tarjeta.fecha_caducidad,
        "cvc": tarjeta.cvc,
        "tipo": tarjeta.tipo,
        "numeroTarjeta": tarjeta.numero_tarjeta,
        "limiteOnline": tarjeta.limite_online, 
        "limiteFisico": tarjeta.limite_fisico, 
    }

@router.put("/actualizar-limites-tarjeta", response_model=LimitesResponse)
async def actualizar_limites_tarjeta(
    request: ActualizarLimitesRequest,
    db: Session = Depends(database.get_db)
):
    # Buscar la tarjeta por teléfono
    tarjeta = db.query(Tarjeta).filter(Tarjeta.telefono_usuario == request.telefono).first()

    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    if request.limite_online <= 0 or request.limite_fisico <= 0:
        raise HTTPException(status_code=400, detail="Los límites deben ser valores positivos")

    # Actualizar los límites
    tarjeta.limite_online = request.limite_online
    tarjeta.limite_fisico = request.limite_fisico

    db.commit()
    db.refresh(tarjeta)

    return LimitesResponse(
        message="Límites de la tarjeta actualizados correctamente",
        numeroTarjeta=tarjeta.numero_tarjeta,
        nuevoLimiteOnline=tarjeta.limite_online,
        nuevoLimiteFisico=tarjeta.limite_fisico
    )