from fastapi import Response, status, Request, Depends
from passlib.context import CryptContext
from app.utils.authJwt import get_user_by_email
from app.utils.audit import save_login


# def validate_user(username, password, response, request):
#     user = get_user_by_email(username)
#     #pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     print(f"Usuario encontrado: {user}")

#     if user is None:
#         response.status_code = status.HTTP_401_UNAUTHORIZED  # Cambiado de 404 a 401
#         response.body = b"Credenciales invalidas 1"
#         return None

#     if not pwd_context.verify(password, user.clave):
#         response.status_code = status.HTTP_401_UNAUTHORIZED  # Cambiado de 404 a 401
#         response.body = b"Credenciales invalidas 2"
#         return None

#     Si todo está bien, guarda el registro del login
#     save_login(user.user_id, user.ente_id, request.client.host)

#     return user

def validate_user(email, password, response, request):
    user = get_user_by_email(email)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print(f"Usuario encontrado: {user}")  # Depuración

    if user is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        response.body = b"Invalid credentials 2"
        return None

    # Depuración de las contraseñas
    print(f"Contraseña proporcionada: {password}")
    print(f"Contraseña almacenada (hasheada): {user.clave}")

    if not pwd_context.verify(password, user.clave):
        print(f"Contraseña no coincide. Verificación fallida.")  # Depuración
        response.status_code = status.HTTP_401_UNAUTHORIZED
        response.body = b"Invalid credentials 3"
        return None

    # Si todo está bien, guarda el registro del login
    save_login(user.user_id, user.ente_id, request.client.host)

    return user

