from typing import List
from pydantic import BaseModel

class BizumRequest(BaseModel):
    telefono_emisor: str
    telefono_receptor: str
    cantidad: float
    concepto: str

class TranferenciaRequest(BaseModel):
    iban_emisor: str
    iban_receptor: str
    cantidad: float
    concepto: str

class AñadirDineroRequest(BaseModel):
    telefono: str
    cantidad: float

class OperacionResponse(BaseModel):
    message: str
    saldo_actual: float

class BalanceDineroResponse(BaseModel):
    ingresos: List[float]
    gastos: List[float]
    meses: List[str]