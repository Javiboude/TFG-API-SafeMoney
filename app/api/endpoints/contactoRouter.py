from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.db.database as database
from app.services.contactoService import ContactoService


router = APIRouter(prefix="", tags=["Contactos"])

@router.get("/contactos/{user_id}")
def get_contactos(user_id: int, db: Session = Depends(database.get_db)):
    service = ContactoService(db)
    contactos = service.get_contactos(user_id)
    return {"contactos": [contacto.nombre_contacto for contacto in contactos]}