import random
import string
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generar_valor_alfanumerico(longitud: int) -> str:
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choices(caracteres, k=longitud))


def hash_password(password: str) -> str:
    return password_context.hash(password)