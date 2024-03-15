from prisma.types import UserCreateInput, _UserWhereUnique_email_Input

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from prisma.enums import Permission
from passlib.context import CryptContext  # type: ignore


from infra.prisma import getPrisma  # type: ignore

signup_router = APIRouter(prefix="/signup", tags=["sign-up"])

prisma = getPrisma()


class Signup(BaseModel):
    password: str
    email: str
    firstname: str
    lastname: str


def hash_password(password: str) -> str:
    return CryptContext(schemes=["bcrypt"]).hash(password)


@signup_router.post("")
async def sign_up(signup_data: Signup):
    already_existing_user = await prisma.user.find_unique(
        where=_UserWhereUnique_email_Input(email=signup_data.email)
    )
    if already_existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    hashed_password = hash_password(signup_data.password)
    try:
        await prisma.user.create(
            data=UserCreateInput(
                email=signup_data.email,
                firstname=signup_data.firstname,
                lastname=signup_data.lastname,
                permission=Permission.User,
                password=hashed_password,
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while creating user : {e}",
        )

    return {}
