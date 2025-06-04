from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.schemas.usuarioSchema import BalanceDineroResponse
from app.schemas.transaccionSchema import BizumRequest, TranferenciaRequest, AñadirDineroRequest, OperacionResponse
from app.services.contactoService import ContactoService
from app.services.movimientoService import MovimientoService
from app.services.transaccionService import TransaccionService
from app.services.usuarioService import UsuarioService

router = APIRouter(prefix="", tags=["Transacciones"])

@router.get("/balance-dinero", response_model=BalanceDineroResponse)
async def get_balance_dinero(db: Session = Depends(database.get_db)):
    service = TransaccionService(db)
    balances = service.get_balances()
    
    if not balances:
        raise HTTPException(status_code=404, detail="No se encontraron balances mensuales")
    
    return BalanceDineroResponse(
        ingresos=[balance.ingresos for balance in balances],
        gastos=[balance.gastos for balance in balances],
        meses=[balance.mes for balance in balances]
    )

@router.post("/realizar-bizum", response_model=OperacionResponse)
async def realizar_bizum(bizum: BizumRequest, db: Session = Depends(database.get_db)):
    usuario_service = UsuarioService(db)
    transaccion_service = TransaccionService(db)
    movimiento_service = MovimientoService(db)
    contacto_service = ContactoService(db)

    emisor = usuario_service.get_user_by_phone(bizum.telefono_emisor)
    if not emisor:
        raise HTTPException(status_code=404, detail="Usuario emisor no encontrado")
    receptor = usuario_service.get_user_by_phone(bizum.telefono_receptor)
    if not receptor:
        raise HTTPException(status_code=404, detail="Usuario receptor no encontrado")
    
    # Validaciones de cantidad
    if emisor.dinero < bizum.cantidad:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    if bizum.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser positiva")
    if bizum.cantidad > 1000:
        raise HTTPException(status_code=400, detail="El límite máximo por Bizum es de 1000€")

    # Actualizar saldos
    emisor.dinero -= bizum.cantidad
    receptor.dinero += bizum.cantidad

    # Registrar bizum
    transaccion_service.create_bizum(
        telefono_emisor=bizum.telefono_emisor,
        telefono_receptor=bizum.telefono_receptor,
        cantidad=bizum.cantidad,
        concepto=bizum.concepto
    )

    # Registrar movimiento para el emisor
    movimiento_service.create_movimiento_usuario(
        usuario_id=emisor.id,
        motivo=f"Bizum a {receptor.nombre}",
        lugar="Bizum",
        cantidad=bizum.cantidad,
        es_positiva=False
    )

    # Registrar movimiento para el receptor
    movimiento_service.create_movimiento_usuario(
        usuario_id=receptor.id,
        motivo=f"Bizum de {emisor.nombre}",
        lugar="Bizum",
        cantidad=bizum.cantidad,
        es_positiva=True
    )

    # Añadir como contacto (solo para el emisor)
    contacto_service.create_contacto(
        usuario_id=emisor.id,
        nombre_contacto=receptor.nombre
    )

    db.commit()
    return OperacionResponse(
        message=f"Bizum de {bizum.cantidad}€ a {receptor.nombre} realizado con éxito",
        saldo_actual=emisor.dinero
    )


@router.post("/realizar-transferencia", response_model=OperacionResponse)
async def realizar_transferencia(transferencia: TranferenciaRequest, db: Session = Depends(database.get_db)):
    usuario_service = UsuarioService(db)
    transaccion_service = TransaccionService(db)
    movimiento_service = MovimientoService(db)
    contacto_service = ContactoService(db)


    emisor = usuario_service.get_user_by_iban(transferencia.iban_emisor)
    if not emisor:
        raise HTTPException(status_code=404, detail="Cuenta emisora no encontrada")
    
    receptor = usuario_service.get_user_by_iban(transferencia.iban_receptor)
    if not receptor:
        raise HTTPException(status_code=404, detail="Cuenta receptora no encontrada")
    
    if emisor.dinero < transferencia.cantidad:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    if transferencia.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser positiva")

    emisor.dinero -= transferencia.cantidad
    receptor.dinero += transferencia.cantidad

    transaccion_service.create_transferencia(
        iban_emisor=transferencia.iban_emisor,
        iban_receptor=transferencia.iban_receptor,
        cantidad=transferencia.cantidad,
        concepto=transferencia.concepto
    )

    # ✅ Llamamos al método correcto pasando el usuario_id
    movimiento_service.create_movimiento_usuario(
        usuario_id=emisor.id,
        motivo=f"Transferencia a {receptor.nombre}",
        lugar="Banco",
        cantidad=transferencia.cantidad,
        es_positiva=False
    )

    movimiento_service.create_movimiento_usuario(
        usuario_id=receptor.id,
        motivo=f"Transferencia de {emisor.nombre}",
        lugar="Banco",
        cantidad=transferencia.cantidad,
        es_positiva=True
    )
    

    contacto_service.create_contacto(
        nombre_contacto=receptor.nombre,
        usuario_id=emisor.id
    )

    db.commit()
    db.refresh(emisor)

    return OperacionResponse(
        message=f"Transferencia de {transferencia.cantidad}€ a cuenta {transferencia.iban_receptor} realizada con éxito",
        saldo_actual=emisor.dinero
    )

@router.post("/anadir-dinero", response_model=OperacionResponse)
async def añadir_dinero(request: AñadirDineroRequest, db: Session = Depends(database.get_db)):
    usuario_service = UsuarioService(db)
    movimiento_service = MovimientoService(db)

    if request.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser un valor positivo")

    usuario = usuario_service.get_user_by_phone(request.telefono)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.dinero += request.cantidad
    db.commit()
    db.refresh(usuario)

    # ✅ Ahora usamos el método correcto y pasamos usuario_id
    movimiento_service.create_movimiento_usuario(
        usuario_id=usuario.id,
        motivo="Ingreso manual",
        lugar="App",
        cantidad=request.cantidad,
        es_positiva=True
    )

    return OperacionResponse(
        message=f"Se han añadido {request.cantidad}€ a tu cuenta",
        saldo_actual=usuario.dinero
    )

