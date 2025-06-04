
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import random
from app.models.usuario import Usuario
from app.models.tarjeta import Tarjeta


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()
    
    def get_user_by_phone(self, telefono: str):
        return self.db.query(Usuario).filter(Usuario.telefono == telefono).first()
    
    def get_user_by_iban(self, iban: str):
        return self.db.query(Usuario).filter(Usuario.iban == iban).first()
    
    def generate_random_iban(self) -> str:
        country_code = "ES"
        check_digits = "00" 
        bank_code = f"{random.randint(1000, 9999):04}"  
        branch_code = f"{random.randint(1000, 9999):04}"
        account_number = f"{random.randint(1000000000, 9999999999):010}" 
        return f"{country_code}{check_digits}{bank_code}{branch_code}{account_number}"

    def create_user(self, nombre: str, telefono: str, password: str, dinero: float):
        db_user = self.get_user_by_phone(telefono)
        if db_user:
            raise HTTPException(status_code=400, detail="El número de teléfono ya está registrado")
        
        iban = self.generate_random_iban()
        
        new_user = Usuario(
            nombre=nombre, 
            telefono=telefono, 
            password=password, 
            dinero=dinero, 
            iban=iban
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        # Creamos la tarjeta asociada al usuario recién creado
        self.create_card_for_user(new_user.telefono, new_user.iban)

        return new_user

    def generate_card_number(self) -> str:
        return f"4{random.randint(10000000000000, 99999999999999):015}"  # Visa (16 dígitos)

    def generate_expiry_date(self) -> str:
        now = datetime.now()
        month = now.month
        year = (now.year + 3) % 100  # Últimos dos dígitos del año
        return f"{month:02d}/{year:02d}"

    def generate_cvc(self) -> str:
        return f"{random.randint(100, 999)}"

    def create_card_for_user(self, telefono_usuario: str, cuenta_asociada: str):
        new_card = Tarjeta(
            telefono_usuario=telefono_usuario,
            cuenta_asociada=cuenta_asociada,
            numero_tarjeta=self.generate_card_number(),
            fecha_caducidad=self.generate_expiry_date(),
            cvc=self.generate_cvc(),
            tipo="Débito",
            limite_online=1000.00,
            limite_fisico=2000.00
        )
        self.db.add(new_card)
        self.db.commit()
        self.db.refresh(new_card)
        return new_card

    def login_user(self, telefono: str, password: str):
        user = self.get_user_by_phone(telefono)
        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Teléfono o contraseña incorrectos")
        return user