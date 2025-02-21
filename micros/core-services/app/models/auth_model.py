from typing import Dict
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    iss: str = None


class ValidateTokenPayload(BaseModel):
    token: str = None

class AuthResponse(BaseModel):
            nombre: str
            email: str
            id: int
            permisos: Dict
            access_token: str