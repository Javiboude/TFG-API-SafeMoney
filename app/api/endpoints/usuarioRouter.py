from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuarioSchema import LoginRequest, LoginResponse, UsuarioResponse
import app.db.database as database
from app.services.usuarioService import UsuarioService

router = APIRouter(prefix="", tags=["Usuarios"])

@router.get("/datos-usuario/{telefono}", response_model=UsuarioResponse)
async def get_datosUsuario(telefono: str, db: Session = Depends(database.get_db)):
    usuario_service = UsuarioService(db)
    user = usuario_service.get_user_by_phone(telefono)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse(
        id=user.id,
        nombre=user.nombre,
        dinero=user.dinero,
        iban=user.iban,
        password=user.password 
    )

@router.post("/register")
def register_user(
    nombre: str,
    telefono: str,
    password: str,
    dinero: float,
    db: Session = Depends(database.get_db)
):
    usuario_service = UsuarioService(db)
    try:
        new_user = usuario_service.create_user(nombre, telefono, password, dinero)
        return {
            "message": "Usuario registrado correctamente con tarjeta asociada",
            "user_id": new_user.id,
            "tarjeta_asociada": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(database.get_db)):
    usuario_service = UsuarioService(db)
    user = usuario_service.login_user(login_data.telefono, login_data.password)
    return {
        "message": "Login exitoso",
        "user_id": user.id,
        "nombre": user.nombre,
    }