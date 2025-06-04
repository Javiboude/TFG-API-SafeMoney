from sqlalchemy.orm import Session
from datetime import datetime
from app.models.contacto import Contacto


class ContactoService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_contactos(self, usuario_id: int):
        return self.db.query(Contacto).filter(
            Contacto.usuario_id == usuario_id
        ).order_by(Contacto.created_at.desc()).all()
    
    def create_contacto(self, usuario_id: int, nombre_contacto: str):
        db_contacto = Contacto(
            usuario_id=usuario_id,
            nombre_contacto=nombre_contacto,
            created_at=datetime.now()
        )
        self.db.add(db_contacto)
        self.db.commit()
        self.db.refresh(db_contacto)
        return db_contacto
