import os
from uuid import uuid4 as uuid
from datetime import datetime, timedelta
from typing import Any, Union
from fastapi import Depends, HTTPException, status
from jose import jwt
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from ..config import get_env
from ..mysql import Database
from ..models.usuario_model import UsuarioModel
from ..models.auth_model import TokenPayload



ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1440 minutes = 24 horas
ALGORITHM = "HS256"
# should be kept secret
JWT_SECRET_KEY = get_env().JWT_SECRET_KEY
# should be kept secret
JWT_REFRESH_SECRET_KEY = get_env().JWT_REFRESH_SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(clave: str) -> str:
    return pwd_context.hash(clave)


def verify_password(clave: str, hashed_pass: str) -> bool:
    hashed_pass = hashed_pass.strip()
    print(f"Contraseña en texto plano: '{clave}'")
    print(f"Hash almacenado: '{hashed_pass}'")
    result = pwd_context.verify(clave, hashed_pass)
    print(f"Resultado de la verificación: {result}")
    return result


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
    to_encode = {"exp": expires_delta, "sub": str(subject), "iss": get_env().MICROS_HASH}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")
def get_user_by_email(email: str):
    with Database() as db:
        
        try:
            query = """
                SELECT 
                    id_usuario, 
                    nombre, 
                    email, 
                    clave,  
                    id_perfil,
                    fecha_creacion 
                FROM 
                    usuarios u 
                WHERE 
                    u.email = %s"""
            db.execute(query, (email,))
            user = db.fetchone()
            
            if not user:
                return None
            
            usuario = UsuarioModel()
            usuario.id_usuario = user[0]
            usuario.nombre = user[1]
            usuario.email = user[2]
            usuario.clave = user[3]
            usuario.id_perfil = user[4]
            usuario.fecha_creacion = user[5]
            print(f"Usuario error: {usuario}")
            return usuario
        except Exception as e:
            print(e)
            return None
        
def get_current_user(token: str = Depends(reuseable_oauth)):
    print("Token recibido:", token)
    
    if token.count(".") != 2:  # Un JWT válido tiene exactamente 2 puntos (3 segmentos)
        print("❌ El token recibido no tiene el formato correcto")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload recibido:", payload)
        
        token_data = TokenPayload(**payload)
        
        print("Fecha de expiración del token:", datetime.fromtimestamp(payload["exp"]))
        print("Hora actual del servidor:", datetime.now())

        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            print("✅ Token expirado")  # ✅ Agrega esto para ver si el problema es el tiempo
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )


        user = get_user_by_email(token_data.sub)
        print("Usuario encontrado en la BD:", user)

        print("Issuer en el token:", token_data.iss)
        print("Issuer esperado:", get_env().MICROS_HASH)

        if token_data.iss is None or token_data.iss != get_env().MICROS_HASH:
            print("❌ Emisor del token incorrecto")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token issuer",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except  (jwt.JWTError, ValidationError):
        print("❌ Error al validar el token:")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def get_permisos(id_perfil: str):
    permisos = {}
    try:
        # Establecer conexión a la base de datos
        with Database() as db:
            query = """

                SELECT 
                    m.nombre_perfil,
                    p.nombre_permiso
                FROM permisos_perfiles pp
                JOIN permisos p ON pp.id_permiso = p.id_permiso
                JOIN perfiles m ON pp.id_perfil = m.id_perfil
                WHERE pp.id_perfil = %s;

            """
            db.execute(query, (id_perfil,))
            results = db.fetchall()

            for result in results:
                perfil = result[0]
                permiso = result[1]

                if perfil not in permisos:
                    permisos[perfil] = []

                permisos[perfil].append(permiso)

            return permisos

    except Exception as e:
        print(e)
        return None