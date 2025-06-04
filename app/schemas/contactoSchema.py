from pydantic import BaseModel
from typing import List

class ContactosResponse(BaseModel):
    contactos: List[str]