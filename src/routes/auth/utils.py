import os

from datetime import datetime, timedelta, UTC
from typing import Annotated


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore

from prisma.models import User
from prisma.types import UserWhereInput
from prisma.enums import Permission
from dotenv import load_dotenv

from infra.prisma import getPrisma  # type: ignore

auth_router = APIRouter(tags=["auth"])

prisma = getPrisma()

if os.getenv("MODE", "dev") == "dev":
    load_dotenv("../.env")


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """
    Make a route require authentication. Return the username of the user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": status.HTTP_401_UNAUTHORIZED,
            "message": "Could not validate credentials",
        },
        headers={},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["username"]
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    except KeyError:
        raise credentials_exception


async def check_admin(username: Annotated[str, Depends(check_token)]) -> None:
    """
    Make a route require admin authentication.
    """
    current_user = await prisma.user.find_unique(
        where=UserWhereInput(email=username)
    )
    if current_user.permission != Permission.Admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": status.HTTP_403_FORBIDDEN,
                "message": "Admin privilege required",
            },
            headers={},
        )


async def check_user(username: Annotated[str, Depends(check_token)]) -> User:
    current_user = await prisma.user.find_unique(
        where=UserWhereInput(email=username),
    )

    if current_user is None:
        raise HTTPException(
            status_code=400, detail="Cannot find the current user id"
        )
    return current_user
