from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from ..controllers.auth_controller import validate_user
from ..utils.authJwt import (create_access_token, 
    get_current_user, 
    get_permisos,
    get_current_user)
from ..mysql import Database
from ..models.auth_model import ValidateTokenPayload

router = APIRouter()

#endpoint para autenticaciónde usuarios
@router.post("/login", summary="create access token for user")
def login(user: OAuth2PasswordRequestForm = Depends(), response: Response = None, request: Request = None):
    usuario = validate_user(user.username, user.password, response, request)
    if usuario is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Credenciales invalidas 3"}

    return {
        "usuario": {
            "nombre": usuario.nombre,
            "email": usuario.email,
            "id": usuario.id_usuario,
            "permisos": get_permisos(usuario.id_perfil),
            "access_token": create_access_token(usuario.email),
        },
    }
    
@router.post("/refresh", summary="create access token for user")
def refresh(data: ValidateTokenPayload, response: Response = None):

    usuarios = get_current_user(data.token)
    if usuarios is False:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return {
        "usuario": {
            "nombre": usuarios.nombre,
            "email": usuarios.email,
            "id": usuarios.id_usuario,
            "permisos": get_permisos(usuarios.id_perfil),
        },
    }