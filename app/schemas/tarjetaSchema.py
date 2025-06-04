from pydantic import BaseModel

class InfoTarjetaResponse(BaseModel):
    saldoCuenta: str
    titular: str
    cuentaAsociada: str
    fechaCaducidad: str
    cvc: str
    tipo: str
    numeroTarjeta: str 
    limiteOnline: float 
    limiteFisico: float

class ActualizarLimitesRequest(BaseModel):
    telefono: str
    limite_online: float
    limite_fisico: float

class LimitesResponse(BaseModel):
    message: str
    numeroTarjeta: str
    nuevoLimiteOnline: float
    nuevoLimiteFisico: float