from pydantic import BaseModel
from typing import List

class BalanceDineroResponse(BaseModel):
    ingresos: List[float]
    gastos: List[float]
    meses: List[str]

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    dinero: float
    iban: str
    password: str

class LoginRequest(BaseModel):
    telefono: str
    password: str 

class LoginResponse(BaseModel):
    message: str
    user_id: int
    nombre: str