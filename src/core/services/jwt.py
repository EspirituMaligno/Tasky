import datetime
from fastapi import HTTPException
from jose import jwt
from config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=15
    )
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.PRIVATE_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True},
        )
        token_type = payload.get("type")

        if token_type not in ["access", "refresh"]:
            raise HTTPException(status_code=401, detail="Invalid token type")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
