import os

from passlib.context import CryptContext

# TODO: Save these values as secrets in ENV file
# This is actually for JWTs
SECRET_KEY = "1d61bbeae422d8857bf4f71385bbc5d03bc56173ef5f23a33b4910fdb1d9aab5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
