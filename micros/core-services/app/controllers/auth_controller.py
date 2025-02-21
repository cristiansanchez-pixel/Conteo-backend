from fastapi import Response, status, Request, Depends
from passlib.context import CryptContext
from app.utils.authJwt import get_user_by_email, get_permisos, get_current_user, create_access_token
from app.utils.audit import save_login
from ..models.auth_model import AuthResponse


def validate_user(username, password, response, request)->AuthResponse:
    
    user = get_user_by_email(username)
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print(f"Usuario encontrado: {user}")
    
    if user is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED  # Cambiado de 404 a 401
        response.body = b"Credenciales invalidas 1"
        return None

    if not pwd_context.verify(password, user.clave):
        response.status_code = status.HTTP_401_UNAUTHORIZED  # Cambiado de 404 a 401
        response.body = b"Credenciales invalidas 2"
        return None

    #Si todo está bien, guarda el registro del login
    save_login(user.id_usuario, request.client.host)
    response = AuthResponse(**user.__dict__,id=user.id_usuario,permisos=get_permisos(user.id_perfil), access_token = create_access_token(user.email))
    response.email = user.email
    response.id = user.id_usuario
    response.nombre= user.nombre
    print(get_permisos(user.id_perfil))
    response.permisos = get_permisos(user.id_perfil)
    response.access_token = create_access_token(user.email)
   
    return response
