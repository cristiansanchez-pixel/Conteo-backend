from fastapi import Response, status, Request
from passlib.context import CryptContext
from app.utils.authJwt import get_user_by_email
from app.utils.audit import save_login


def validate_user(email: str, password: str, response: Response, request: Request):
    user = get_user_by_email(email)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if user is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if not pwd_context.verify(password, user.user_password):
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    if user.user_status != "active":
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return None

    save_login(user.user_id, user.ente_id, request.client.host)

    return user