from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from ..controllers.auth_controller import validate_user
from ..utils.authJwt import (create_access_token, 
    get_current_user, 
    get_permisos,
    get_current_user)
from ..mysql import Database
from ..models.auth_model import ValidateTokenPayload, AuthResponse

router = APIRouter()

#endpoint para autenticaciónde usuarios
@router.post("/login", summary="create access token for user")
def login(user: OAuth2PasswordRequestForm = Depends(), response: Response = None, request: Request = None) -> AuthResponse:
    usuario = validate_user(user.username, user.password, response, request)
    if usuario is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Credenciales invalidas 3"}
    return usuario
   

    
    
@router.post("/refresh", summary="Refresh access token")
def refresh(data: ValidateTokenPayload):
    # Verificar si el token es válido
    usuario = get_current_user(data.token)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Generar un nuevo access_token
    new_access_token = create_access_token({"sub": usuario.id_usuario})

    # Devolver el nuevo token y los datos del usuario
    return JSONResponse(
        content={
            "access_token": new_access_token,
            "token_type": "bearer",
            "usuario": {
                "nombre": usuario.nombre,
                "email": usuario.email,
                "id": usuario.id_usuario,
                "permisos": get_permisos(usuario.id_perfil),
            },
        },
        status_code=status.HTTP_200_OK
    )