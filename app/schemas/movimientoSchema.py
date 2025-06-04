from pydantic import BaseModel
from typing import List

class Movimiento(BaseModel):
    id: int
    motivo: str
    lugar: str
    cantidad: float
    esPositiva: bool

class UltimosMovimientosResponse(BaseModel):
    movimientos: List[Movimiento]